import pandas as pd

from utils import save_and_compress, select_and_clean

"""
Legislation from Luxembourg in fr
"""

jurisdictions_judiciaires = pd.read_json('juridictions_judiciaires.jsonl', lines=True)
judoc = pd.read_json('judoc.jsonl', lines=True)
df = pd.concat([jurisdictions_judiciaires, judoc])

df['type'] = 'caselaw'
df['jurisdiction'] = 'Luxembourg'
df = select_and_clean(df)
save_and_compress(df, 'judoc')
