import datetime
import re
from urllib.parse import urlparse

import pandas as pd
from datasets import load_dataset

mc4 = load_dataset("mc4", languages=['de'], streaming=True)['train']

base_terms = [r'Art\.\s*\d+', r'Abs\.\s*\d+', r'§']
latin_terms = ['in casu', 'de lege lata', 'de lege ferenda', ]
additional_terms = ['Richter', 'Anwalt', 'Rechtssprechung', 'Verjährungsfrist', 'Verwirkungsfrist', 'Berufung',
                    'Beschwerdeführer', 'Kläger', 'Beschwerdegegner']
terms = base_terms + latin_terms + additional_terms
search_terms = '|'.join(terms)  # combine list into one regex for performance reasons

print(f"Searching for {search_terms} in mc4")


def status_update():
    global begin_time
    print(f"Found at least one of the search terms in {len(legal_mc4)} documents from {index + 1} searched.")
    print(f"Blocked domains: {blocked_domains}")
    print(f"This iteration took {datetime.datetime.now() - begin_time}")
    print()
    begin_time = datetime.datetime.now()


begin_time = datetime.datetime.now()
blocked_domains = []  # add domains here which contain with high probability no legal text
domains = {}  # contains one entry per domain
confidence = 100
threshold = 0.8
legal_mc4 = list()
for index, doc in enumerate(mc4):
    domain = urlparse(doc['url']).netloc
    if domain in blocked_domains:  # as soon as a domain is in blocked_domains, skip the document
        continue

    if domain not in domains:
        domains[domain] = {"legal": 0, "non_legal": 0}  # add new empty entry for domain

    if re.search(search_terms, doc['text']):  # search terms in document
        legal_mc4.append(doc)
        domains[domain]["legal"] += 1
    else:
        domains[domain]["non_legal"] += 1

    legal_num, non_legal_num = domains[domain]["legal"], domains[domain]["non_legal"]
    total = legal_num + non_legal_num

    if total >= confidence and non_legal_num / total > threshold:
        blocked_domains.append(domain)

    if index % 1e5 == 0:
        status_update()

status_update()

df = pd.DataFrame(legal_mc4)
df.to_json('data/legal_mc4.jsonl', orient='records', lines=True)

# Analyze the links the documents came from
# df = pd.read_json('data/legal_mc4.jsonl', lines=True)
df.url = df.url.apply(lambda x: urlparse(x).netloc)
print(df.url.unique())
