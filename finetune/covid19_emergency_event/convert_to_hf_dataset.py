import os
from pathlib import Path

import pandas as pd

label_cols = [f"event{i}"  for i in range(1,9)]

data_path = Path("COVID19_emergency_event-main/annotations")

train = pd.read_csv(data_path / "all_train_or.tsv", sep='\t', index_col="id")
validation = pd.read_csv(data_path / "all_dev_or.tsv", sep='\t', index_col="id")
test = pd.read_csv(data_path / "all_test_or.csv", sep='\t', index_col="id")  # yes, it also has the tab as separator


# save splits
def save_splits_to_jsonl(config_name):
    # save to jsonl files for huggingface
    if config_name: os.makedirs(config_name, exist_ok=True)
    train.to_json(os.path.join(config_name, "train.jsonl"), lines=True, orient="records", force_ascii=False)
    validation.to_json(os.path.join(config_name, "validation.jsonl"), lines=True, orient="records", force_ascii=False)
    test.to_json(os.path.join(config_name, "test.jsonl"), lines=True, orient="records", force_ascii=False)


save_splits_to_jsonl("")

def print_split_table_multi_label(splits, label_names):
    data = {split_name: {} for split_name in splits.keys()}
    for split_name, split in splits.items():
        sum = 0
        for label_name in label_names:
            counts = split[label_name].value_counts()
            data[split_name][label_name] = counts[True] if True in counts else 0
            sum += data[split_name][label_name]
        data[split_name]["total occurrences"] = sum
        data[split_name]["split size"] = len(split.index)
    table = pd.DataFrame(data)

    print(table.to_markdown())


print_split_table_multi_label({"train": train, "validation": validation, "test": test}, label_cols)

