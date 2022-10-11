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


def process_data(df, type):
    if type == 'caselaw':
        cols_to_remove = ['id', 'slug', 'court', 'file_number', 'date', 'created_date', 'updated_date', 'type', 'ecli']
    if type == 'legislation':
        cols_to_remove = ['id', 'book', 'title', 'slug', 'created_date', 'updated_date',
                          'section', 'amtabk', 'kurzue', 'doknr', 'order']
    df = df.rename_column('content', 'text')
    df = df.remove_columns(cols_to_remove)
    df = df.filter(lambda example: len(example['text']) > 100)

    df = df.map(parse_text, num_proc=16)

    df = df.add_column("type", [type] * len(df))
    df = df.add_column("language", ["de"] * len(df))
    df = df.add_column("jurisdiction", ["Germany"] * len(df))

    save_and_compress(df, f'german_{type}')


process_data(load_dataset('json', data_files='data/cases.jsonl')['train'], 'caselaw')
process_data(load_dataset('json', data_files='data/laws.jsonl')['train'], 'legislation')
