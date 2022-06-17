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

# split sizes: train 3501, validation 442, test 442
print("train split size: ", len(train.index))
print("validation split size: ", len(validation.index))
print("test split size: ", len(test.index))
