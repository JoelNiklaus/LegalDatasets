import pandas as pd

from utils import save_and_compress, select_and_clean
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

"""
Legislation from the UK in en (https://zenodo.org/record/6355465)
"""
df = pd.read_json('uk-lex18.jsonl', lines=True)
df['language'] = 'en'
df['type'] = 'legislation'
df['jurisdiction'] = 'UK'
df = df.rename(columns={"body": "text"})

df = select_and_clean(df)

save_and_compress(df, f'uk_legislation')

