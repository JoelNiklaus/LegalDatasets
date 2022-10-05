import os

import pandas as pd
import datasets


def save_and_compress(dataset, court, idx):
    if idx:
        path = f"{court}_{idx}.jsonl"
    else:
        path = f"{court}.jsonl"
    dataset.to_json(path, force_ascii=False)

    print("Compressing...")
    os.system(f'xz -zkf -T0 {path}')  # -TO to use multithreading


for court in ["ConCo", "SupAdmCo", "SupCo"]:
    df = pd.read_csv(f"{court}.csv", names=["file_name", "docket_number", "date", "court_abbreviation"],
                     encoding='latin-1')
    print(df)
    df["text"] = df.file_name.apply(lambda x: open(f"{court}/{x}", "r", encoding='latin-1').read().strip())
    print(df)
    df.drop(columns=["court_abbreviation"], inplace=True)
    dataset = datasets.Dataset.from_pandas(df)
    save_and_compress(dataset, court, None)
