import datasets
import pandas as pd

from utils import save_and_compress

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

"""
Caselaw from Switzerland in de, fr and it
"""
dataset = datasets.load_dataset("json", data_files=f"train.jsonl")["train"]

print(dataset)
print(dataset.column_names)

dataset = dataset.add_column("type", ["caselaw"] * len(dataset))
dataset = dataset.add_column("jurisdiction", ["Switzerland"] * len(dataset))

cols_to_remove = ['decision_id', 'year', 'chamber', 'court', 'canton', 'region', 'legal_area']
dataset = dataset.rename_column('full_text', 'text')
dataset = dataset.remove_columns(cols_to_remove)
dataset = dataset.filter(lambda example: len(example['text']) > 100)

for language in ['de', 'fr', 'it']:
    lang_dataset = dataset.filter(lambda example: example['language'] == language)
    save_and_compress(lang_dataset, f'swiss_caselaw_{language}')
