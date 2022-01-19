import datetime
import json
import re
from urllib.parse import urlparse

import pandas as pd
from datasets import load_dataset

# TODO download more data at a time ==> streaming and decompressing is the bottleneck
mc4 = load_dataset("mc4", languages=['de'], streaming=True)['train']

base_terms = [r'Art\.\s*\d+', r'Abs\.\s*\d+', r'§\s*\d+']
latin_terms = ['in casu', 'de lege lata', 'de lege ferenda', ]
additional_terms = ['Richter', 'Anwalt', 'Gerichtshof', 'Rechtssprechung', 'Verjährungsfrist', 'Verwirkungsfrist',
                    'Berufung', 'Beschwerdeführer', 'Kläger', 'Beschwerdegegner']
terms = base_terms + latin_terms + additional_terms
search_terms = re.compile('|'.join(terms))  # combine list into one regex for performance reasons

# TODO also create blacklist words

print(f"Searching for {search_terms} in mc4")

text_path = 'data/legal_mc4.csv'
progress_path = 'data/progress.json'


def status_update(index):
    global begin_time
    print(
        f"Found at least {min_num_matches} of the search terms "
        f"in {len(legal_mc4['index'])} documents from {index + 1} searched.")
    print(f"Blocked domains: {[domain for domain, value in domains.items() if value['blocked']]}")
    print(f"This iteration took {datetime.datetime.now() - begin_time}")
    print()
    begin_time = datetime.datetime.now()


def save_and_reset(texts):
    print(f"Saving {batch_size} texts to the file system")
    df = pd.DataFrame(texts)
    df.to_csv(text_path, mode='a', header=False)
    return {"url": [], "text": [], "timestamp": [], "index": []}


def save_and_report_progress(legal_mc4, current_index):
    legal_mc4 = save_and_reset(legal_mc4)
    status_update(current_index)
    domains['current_index'] = current_index
    with open(progress_path, 'w') as outfile:
        json.dump(domains, outfile)
    del domains['current_index']  # to cause no problems in status_update
    return legal_mc4


domains = {}  # contains one entry per domain
confidence = 1000
threshold = 0.99  # we don't want to miss out on texts
min_num_matches = 5
batch_size = 1e5

legal_mc4 = {"url": [], "text": [], "timestamp": [], "index": []}
df = pd.DataFrame(legal_mc4)
df.to_csv(text_path)

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
        legal_mc4["url"].append(doc["url"])
        legal_mc4["text"].append(doc["text"])
        legal_mc4["timestamp"].append(doc["timestamp"])
        legal_mc4["index"].append(index)
        domains[domain]["legal"] += 1
    else:
        domains[domain]["non_legal"] += 1

    legal_num, non_legal_num = domains[domain]["legal"], domains[domain]["non_legal"]
    total = legal_num + non_legal_num

    if total >= confidence and non_legal_num / total > threshold:
        domains[domain]["blocked"] = True

    if index % batch_size == 0:
        legal_mc4 = save_and_report_progress(legal_mc4, index)

save_and_report_progress(legal_mc4, index)
