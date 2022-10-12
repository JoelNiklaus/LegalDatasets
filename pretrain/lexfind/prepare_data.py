import pandas as pd
from bs4 import BeautifulSoup

from utils import save_and_compress, select_and_clean
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

"""
Legislation from Switzerland in de, fr, it, en and rm
"""
# somehow it doesn't work with datasets: https://github.com/huggingface/datasets/issues/3965
#dataset = datasets.load_dataset("json", data_files=f"lexfind.jsonl")["train"]

def parse_text(example):
    if example['html_content']:
        example['text'] = BeautifulSoup(example['html_content'], features="lxml").get_text()
    else:
        example['text'] = example['pdf_content']
    return example

df = pd.read_json('lexfind.jsonl', lines=True)
df['type'] = 'legislation'
df['jurisdiction'] = 'Switzerland'
df = df.apply(parse_text, axis="columns")
df = select_and_clean(df)

for language in df.language.unique().tolist():
    lang_df = df[df.language.str.contains(language)]
    save_and_compress(lang_df, f'swiss_legislation_{language}')
