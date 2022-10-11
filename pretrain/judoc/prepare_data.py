import pandas as pd

from utils import save_and_compress

"""
Legislation from Belgium in fr and nl
"""

jurisdictions_judiciaires = pd.read_json('juridictions_judiciaires.jsonl', lines=True)
judoc = pd.read_json('judoc.jsonl', lines=True)
df = pd.concat([jurisdictions_judiciaires, judoc])

df['type'] = 'caselaw'
df['jurisdiction'] = 'Luxembourg'
df = df[['type', 'language', 'jurisdiction', 'text']]
df.dropna(subset=['text'], inplace=True)  # remove nans
df = df[df['text'].str.len() > 100]  # remove very small instances
save_and_compress(df, 'judoc')
