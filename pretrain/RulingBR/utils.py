import os
from typing import Union

import datasets
import pandas as pd


def save_and_compress(dataset: Union[datasets.Dataset,pd.DataFrame], name: str, idx=None):
    if idx:
        path = f"{name}_{idx}.jsonl"
    else:
        path = f"{name}.jsonl"

    print("Saving to", path)
    dataset.to_json(path, force_ascii=False, orient='records', lines=True)

    print("Compressing...")
    os.system(f'xz -zkf -T0 {path}')  # -TO to use multithreading
