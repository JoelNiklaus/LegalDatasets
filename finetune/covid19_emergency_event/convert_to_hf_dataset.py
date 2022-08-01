import os
from pathlib import Path

import pandas as pd

# run pip install wget and pip install fasttext-langdetect for this to work
from ftlangdetect import detect

label_cols = [f"event{i}" for i in range(1, 9)]

data_path = Path("COVID19_emergency_event-main/annotations")

countries = ["belgium", "france", "hungary", "italy", "netherlands", "norway", "poland", "uk"]

train, validation, test = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

for country in countries:
    country_train = pd.read_csv(data_path / country / "train_or.tsv", sep='\t', index_col="id")
    country_validation = pd.read_csv(data_path / country / "dev_or.tsv", sep='\t', index_col="id")
    country_test = pd.read_csv(data_path / country / "test_or.tsv", sep='\t', index_col="id")

    country_train["country"] = country
    country_validation["country"] = country
    country_test["country"] = country

    train = train.append(country_train)
    validation = validation.append(country_validation)
    test = test.append(country_test)

# train = pd.read_csv(data_path / "all_train_or.tsv", sep='\t', index_col="id")
# validation = pd.read_csv(data_path / "all_dev_or.tsv", sep='\t', index_col="id")
# test = pd.read_csv(data_path / "all_test_or.csv", sep='\t', index_col="id")  # yes, it also has the tab as separator


country_to_lang = {"belgium": "fr", "france": "fr", "hungary": "hu", "italy": "it", "netherlands": "nl", "norway": "nb",
                   "poland": "pl", "uk": "en"}

# set language
train['language'] = train.country.apply(lambda x: country_to_lang[x])
validation['language'] = validation.country.apply(lambda x: country_to_lang[x])
test['language'] = test.country.apply(lambda x: country_to_lang[x])

# reorder columns
column_list = ["language", "country", "text"]
column_list.extend(label_cols)
train = train[column_list]
validation = validation[column_list]
test = test[column_list]


def aggregate_events(row):
    all_events = []
    for label_col in label_cols:
        if row[label_col]:
            all_events.append(label_col)
    return all_events


train["all_events"] = train.apply(aggregate_events, axis=1)
validation["all_events"] = validation.apply(aggregate_events, axis=1)
test["all_events"] = test.apply(aggregate_events, axis=1)


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
