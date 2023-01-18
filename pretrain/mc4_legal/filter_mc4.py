import argparse
import re
from urllib.parse import urlparse

import datasets
import fsspec
from datasets import load_dataset

import os
import json

from tqdm import tqdm

try:
    import lzma as xz
except ImportError:
    import pylzma as xz

import logging
import sys

root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)
logger = logging.getLogger(__name__)

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


scraped_languages = []
all_languages = ["bg", "cs", "da", "de", "el", "en", "es", "et", "fi", "fr", "ga",
                 "hu", "it", "lt", "lv", "mt", "nl", "pl", "pt", "ro", "sk", "sl", "sv"]  # mc4 does not contain "hr"
new_languages = list(set(all_languages) - set(scraped_languages))

debug = False
data_dir = 'data'
os.makedirs(data_dir, exist_ok=True)
confidence = 1000
threshold = 0.99  # we don't want to miss out on texts
min_num_matches = 5
batch_size = 100_000
download_size = 500  # in MiB
MAX_FILE_SIZE = 6.25e8  # 625 MB
NUM_PROCESSES = 16  # seems to be the sweet spot for batch size 100_000
use_domains_filter = True

# download more data at a time ==> streaming and decompressing is the bottleneck
# 5 MiB per Default: 5 * 2 ** 20, increase to 500MiB
fsspec.spec.AbstractBufferedFile.DEFAULT_BLOCK_SIZE = download_size * 2 ** 20

datasets.disable_caching()  # save disk space


def compile_search_terms(language):
    with open('terms.json', 'r') as file:
        terms = json.load(file)
    terms_list = terms['latin']
    logger.info(f"Search terms for {language}: {terms_list}")
    logger.info("ruling")
    if language in terms['ruling']:
        for country_terms in terms['ruling'][language].values():
            logger.info(country_terms)
            # exclude other abbreviations such as BGHW instead of BGH
            terms_list.extend([f"\\s{re.escape(term)}\\s" for term in country_terms])
    else:
        logger.info(f"No search terms found for rulings in {language}")
    logger.info("law")
    if language in terms['law']:
        for country_terms in terms['law'][language].values():
            logger.info(country_terms)
            # add \s*\d+ to reduce false positives, but only here, not with the rulings
            # without this, the result files get huge! (de: 87G, fr: 451G, it: 208G)
            # also they contain a lot of obviously non-legal data (e.g. general forums, general newspaper articles)
            terms_list.extend([f"\\s{re.escape(term)}\\s*\\d+" for term in country_terms])
    else:
        logger.info(f"No search terms found for laws in {language}")
    terms_list = list(set(terms_list))  # remove any duplicates
    return re.compile('|'.join(terms_list), flags=re.IGNORECASE)  # combine list into one regex for performance reasons


def get_output_file_name(language, split='train', file_idx=0):
    # we save each dataset to a separate file, so we only need to generate new datasets
    return f"{data_dir}/{language}.{split}.{file_idx}.jsonl.xz"


def open_new_file(language, split, output_file_idx):
    filename = get_output_file_name(language, split, output_file_idx)
    logger.info(f"Writing to {filename}")
    return xz.open(filename, "wt")  # write mode


def save_domains(domains, language):
    domains_dir = f"{data_dir}/domains"
    os.makedirs(domains_dir, exist_ok=True)
    with open(f"{domains_dir}/{language}.json", 'w') as outfile:
        json.dump(domains, outfile)


"""
One mc4 file has approx. 25K entries
per language: train and validation files  ==> train and validation entries (approx.)
en: 11264, 128 ==> 281_600_000, 3_200_000
de,es,fr: 2048, 16 ==> 51_200_000, 400_000
it: 1024, 8 ==> 25_600_000, 200_000
hu: 1024, 2 ==> 25_600_000, 50_000
sk: 512, 1 ==> 12_800_000, 25_000
lv: 256, 1 ==> 6_400_000, 25_000
mt: 128, 1 ==> 3_200_000, 25_000

==> en: 88 times more train files than mt
==> mt: 128 x 25_000 = 3_200_000 (32 batches)
==> en: 11264 x 25_000 = 281_600_000 (2816 batches)

==> we could start an array job and save each array element to a different file (train.{index}.jsonl.xz
"""


def filter_mc4(language):
    logger.info(f"Filtering mc4 for legal documents in language {language}")
    search_terms = compile_search_terms(language)
    domains = dict()

    def search_regexes(example):
        if use_domains_filter:
            domain = urlparse(example['url']).netloc
            if domain in domains.keys():
                if domains[domain]["blocked"]:  # as soon as a domain is blocked, skip the document
                    return example
            else:  # add new empty entry for domain
                domains[domain] = {"legal": 0, "non_legal": 0, "blocked": False}

        # this is the expensive operation we want to avoid
        matches = re.findall(search_terms, example['text'])  # search terms in document
        if len(matches) > min_num_matches:  # A manual sample search yielded only few false positives
            example['matches'] = matches
            if use_domains_filter:
                domains[domain]["legal"] += 1
        else:
            if use_domains_filter:
                domains[domain]["non_legal"] += 1

        if use_domains_filter and should_domain_be_blocked(domain):
            domains[domain]["blocked"] = True
            logger.info(f"Blocking domain {domain}")
        return example

    def should_domain_be_blocked(domain):
        # check if domain should be blocked
        legal_num, non_legal_num = domains[domain]["legal"], domains[domain]["non_legal"]
        total = legal_num + non_legal_num  # number of times we have seen the domain
        return total >= confidence and non_legal_num / total > threshold

    for split in ['train', 'validation']:
        try:
            mc4_streaming = load_dataset("mc4", languages=[language], streaming=True, split=split)
        except KeyError:
            logger.info(f"No subset of mc4 available for language {language}")
            return
        logger.info(f"Searching for {search_terms} in mc4 {language}")

        output_file_idx, num_legal_docs, num_total_legal_docs = 0, 0, 0
        file = open_new_file(language, split, output_file_idx)
        for idx, example in tqdm(enumerate(mc4_streaming)):
            if idx % batch_size == 0 and idx != 0:
                logger.info(f"Processed {batch_size} documents and found {num_legal_docs} legal documents")
                num_total_legal_docs += num_legal_docs
                logger.info(
                    f"Status so far: {idx} documents processed and {num_total_legal_docs} legal documents found")
                num_legal_docs = 0
            datapoint = search_regexes(example)
            if 'matches' in datapoint:
                if os.path.getsize(get_output_file_name(language, split, output_file_idx)) > MAX_FILE_SIZE:
                    file.close()
                    output_file_idx += 1
                    file = open_new_file(language, split, output_file_idx)
                file.write(json.dumps(datapoint) + "\n")
                num_legal_docs += 1
        file.close()

    if use_domains_filter:
        save_domains(domains, language)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-l', '--languages', help='Define the list of languages', default=None)

    args = parser.parse_args()

    if args.languages is None:
        languages = all_languages
    else:
        languages = args.languages.split(',')

    for language in languages:
        filter_mc4(language)
        # TODO Quality check: look at 100 samples and do iterative filtering
        # TODO remove duplicate texts
        # TODO sort terms.json alphabetically and check if every language is in there
