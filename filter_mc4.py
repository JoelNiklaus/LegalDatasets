import datetime
import json
import re
from pathlib import Path
from urllib.parse import urlparse

import fsspec
import pandas as pd
from datasets import load_dataset

# TODO how to do deduplication: form trigram multiset, they are duplicates if |tri(s1 ) ∩ tri(s2 )| ≥ |tri(s1 )|/2.
# https://pypi.org/project/text-dedup/
# https://towardsdatascience.com/a-laymans-guide-to-fuzzy-document-deduplication-a3b3cf9a05a7
# https://github.com/ekzhu/datasketch: 10 hash functions for each Minhash and an approximate Jaccard similarity of 0.5 (ThePile)
# exact match deduplication (huggingface): calculate hash of document (after removing all whitespace) and only keep unique hashes

# TODO Thomas fragen ob er diese Strings auch für andere Länder und Sprachen erstellen kann
#  Still todo: Netherlands, Denmark, Sweden, Norway, Finland, etc.

# Legalis.ch: Helbing Lichtenhahn (Basler Kommentare)
# Swisslex.ch: Schulthess, und andere Verlage

# Definition von Rechtstexten:
# Von Juristen geschrieben, KEINE Massenmedien bspw. ==> evtl. gewisse Domains sperren
# Hypothese: Rechtstexte enthalten Gesetzeszitierungen (im civil law) Art. oder Abs. oder § oder Urteilszitierungen (im common law) oder beides
# Ausnahmen: evtl. Absätze von Lehrbüchern,

# Abs. könnte False Positives bringen von anderen Zitaten ==> Abs. kommt sehr selten ohne Art. vor
# mit diesen Begriffen müssen wir aufpassen, da wir sonst Gefahr laufen Boulevardpresse zu finden. ==> Keine Rechtstexte
# additional_terms = ['Richter', 'Anwalt', 'Gerichtshof', 'Rechtssprechung', 'Verjährungsfrist', 'Verwirkungsfrist',
#                     'Berufung', 'Beschwerdeführer', 'Kläger', 'Beschwerdegegner']

languages = ["de", "fr", "it", "pl", "sk", "cs", "pt", "es"]
debug = False
data_dir = Path('data')
confidence = 1000
threshold = 0.99  # we don't want to miss out on texts
min_num_matches = 5
batch_size = 1e5
download_size = 500  # in MiB

# download more data at a time ==> streaming and decompressing is the bottleneck
# 5 MiB per Default: 5 * 2 ** 20, increase to 500MiB
fsspec.spec.AbstractBufferedFile.DEFAULT_BLOCK_SIZE = download_size * 2 ** 20

"""
The current search procedure seems to make more or less sense after a manual check of 20 entries.
de: 26G
fr: 11G
it: 12G
pl: 9.3G
sk: 1.3G
cs: 6.8G
pt: 4.5G
es: 20G
"""


def compile_search_terms(language):
    with open('terms.json', 'r') as file:
        terms = json.load(file)
    terms_list = terms['latin']
    print("ruling")
    for country_terms in terms['ruling'][language].values():
        print(country_terms)
        # exclude other abbreviations such as BGHW instead of BGH
        terms_list.extend([term + "\\s" for term in country_terms])
    print("law")
    for country_terms in terms['law'][language].values():
        print(country_terms)
        # add \s*\d+ to reduce false positives, but only here, not with the rulings
        # without this, the result files get huge! (de: 87G, fr: 451G, it: 208G)
        # also they contain a lot of obviously non-legal data (e.g. general forums, general newspaper articles)
        terms_list.extend([term + "\\s*\\d+" for term in country_terms])
    terms_list = list(set(terms_list))  # remove any duplicates
    return re.compile('|'.join(terms_list), flags=re.IGNORECASE)  # combine list into one regex for performance reasons


def filter_mc4(language):
    lang_dir = data_dir / language
    lang_dir.mkdir(parents=True, exist_ok=True)
    text_path = lang_dir / 'legal_mc4.csv'
    progress_path = lang_dir / 'progress.json'

    domains = {}  # contains one entry per domain
    legal_mc4 = {"index": [], "url": [], "timestamp": [], "matches": [], "text": [], }
    df = pd.DataFrame(legal_mc4)
    df.to_csv(text_path)

    search_terms = compile_search_terms(language)
    mc4 = load_dataset("mc4", languages=[language], streaming=True)['train']
    print(f"Searching for {search_terms} in mc4 {language}")

    def status_update(index, begin_time):
        print(
            f"Found at least {min_num_matches} of the search terms "
            f"in {len(legal_mc4['index'])} documents from {index + 1} searched.")
        if debug:
            print(f"Blocked domains: {[domain for domain, value in domains.items() if value['blocked']]}")
        print(f"This iteration took {datetime.datetime.now() - begin_time}")
        print()

    def save_and_reset(texts):
        print(f"Saving {batch_size} texts to the file system")
        df = pd.DataFrame(texts)
        df.to_csv(text_path, mode='a', header=False)
        return {"index": [], "url": [], "timestamp": [], "matches": [], "text": [], }

    def save_and_report_progress(legal_mc4, current_index, begin_time):
        legal_mc4 = save_and_reset(legal_mc4)
        status_update(current_index, begin_time)
        domains['current_index'] = current_index
        with open(progress_path, 'w') as outfile:
            json.dump(domains, outfile)
        del domains['current_index']  # to cause no problems in status_update
        return legal_mc4

    begin_time = datetime.datetime.now()

    for index, doc in enumerate(mc4):
        domain = urlparse(doc['url']).netloc
        if domain in domains.keys() and domains[domain]["blocked"]:  # as soon as a domain is blocked, skip the document
            continue

        if domain not in domains:
            # add new empty entry for domain
            domains[domain] = {"legal": 0, "non_legal": 0, "blocked": False}

        matches = re.findall(search_terms, doc['text'])  # search terms in document
        if len(matches) > min_num_matches:  # A manual sample search yielded only few false positives
            legal_mc4["index"].append(index)
            legal_mc4["url"].append(doc["url"])
            legal_mc4["timestamp"].append(doc["timestamp"])
            legal_mc4["matches"].append(matches)
            legal_mc4["text"].append(doc["text"])
            domains[domain]["legal"] += 1
        else:
            domains[domain]["non_legal"] += 1

        legal_num, non_legal_num = domains[domain]["legal"], domains[domain]["non_legal"]
        total = legal_num + non_legal_num

        if total >= confidence and non_legal_num / total > threshold:
            domains[domain]["blocked"] = True

        if index % batch_size == 0:
            legal_mc4 = save_and_report_progress(legal_mc4, index, begin_time)
            begin_time = datetime.datetime.now()

    save_and_report_progress(legal_mc4, index, begin_time)


if __name__ == '__main__':
    # for language in languages:
    for language in ["pt", "es"]:
        filter_mc4(language)
        # TODO Quality check: look at 100 samples and do iterative filtering
        # TODO remove duplicate texts
