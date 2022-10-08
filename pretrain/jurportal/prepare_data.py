import pandas as pd

from utils import save_and_compress, select_and_clean

"""
Case law from Belgium 
"""

df = pd.read_json('belgium.jsonl', lines=True, orient='records')
print(df.head())
print(df.columns)

df = df.rename(columns={'country': 'jurisdiction', })
df['type'] = 'caselaw'

df = select_and_clean(df)
save_and_compress(df, 'jurportal')
