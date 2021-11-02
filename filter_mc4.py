import re
from urllib.parse import urlparse

import pandas as pd
from datasets import load_dataset

mc4 = load_dataset("mc4", languages=['de'], streaming=True)['train']

base_terms = [r'Art\.\s*\d+', r'Abs\.\s*\d+', r'§']
latin_terms = ['in casu', 'de lege lata', 'de lege ferenda', ]
additional_terms = ['Richter', 'Anwalt', 'Rechtssprechung', 'Verjährungsfrist', 'Verwirkungsfrist', 'Berufung',
                    'Beschwerdeführer', 'Kläger']
terms = base_terms + latin_terms + additional_terms
search_terms = '|'.join(terms)  # combine list into one regex for performance reasons

print(f"Searching for {search_terms} in mc4")


def status_update():
    print(f"Found at least one of the search terms in {len(legal_mc4)} documents from {index + 1} searched.")


legal_mc4 = list()
for index, doc in enumerate(mc4):
    if re.search(search_terms, doc['text']):
        legal_mc4.append(doc)

    if index % 1e5 == 0:
        status_update()

status_update()

df = pd.DataFrame(legal_mc4)
df.to_json('data/legal_mc4.jsonl', orient='records', lines=True)

# Analyze the urls the documents came from
# df = pd.read_json('data/legal_mc4.jsonl', lines=True)
df.url = df.url.apply(lambda x: urlparse(x).netloc)
print(df.url.unique())
