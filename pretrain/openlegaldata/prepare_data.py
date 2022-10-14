import pandas as pd
from bs4 import BeautifulSoup
from datasets import load_dataset

from utils import save_and_compress, select_and_clean

"""
Caselaw and Legislation from Germany in de
"""


def parse_text(example):
    example['text'] = BeautifulSoup(example['text'], features="lxml").get_text()
    return example


def process_data(dataset, type):
    if type == 'caselaw':
        cols_to_remove = ['id', 'slug', 'court', 'file_number', 'date', 'created_date', 'updated_date', 'type', 'ecli']
    if type == 'legislation':
        cols_to_remove = ['id', 'book', 'title', 'slug', 'created_date', 'updated_date',
                          'section', 'amtabk', 'kurzue', 'doknr', 'order']
    dataset = dataset.rename_column('content', 'text')
    dataset = dataset.remove_columns(cols_to_remove)
    dataset = dataset.filter(lambda example: len(example['text']) > 100)

    dataset = dataset.map(parse_text, num_proc=16)

    dataset = dataset.add_column("type", [type] * len(dataset))
    dataset = dataset.add_column("language", ["de"] * len(dataset))
    dataset = dataset.add_column("jurisdiction", ["Germany"] * len(dataset))

    save_and_compress(dataset, f'german_{type}')


process_data(load_dataset('json', data_files='data/cases.jsonl')['train'], 'caselaw')
process_data(load_dataset('json', data_files='data/laws.jsonl')['train'], 'legislation')
