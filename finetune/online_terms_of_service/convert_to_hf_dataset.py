import glob
import os
from pathlib import Path

import pandas as pd

data_path = Path("corpus_NLLP2021")
languages = ["de", "en", "it", "pl"]

file_names = glob.glob(str(data_path / "sentences" / "de" / "original/*"))
companies = sorted([Path(file_name).stem for file_name in file_names])
print(companies)


def get_file_name(type, language, company):
    return data_path / type / language / "original" / (company + ".txt")


def read_lines(file_name):
    with open(file_name) as file:
        return [line.strip() for line in file.readlines()]


def read_companies(languages, companies):
    data = []
    for language in languages:
        for company in companies:
            tags = read_lines(get_file_name("tags", language, company))
            tags = [tuple(tag.split(" ")) for tag in tags]  # make tuples out of tags for easier handling
            sentences = read_lines(get_file_name("sentences", language, company))
            assert len(tags) == len(sentences), "The number of tags is not equal to the number of sentences"
            for i in range(len(tags)):
                row = {"language": language, "company": company, "sentence": sentences[i], "tag": tags[i]}
                data.append(row)
    return pd.DataFrame.from_records(data)


df = read_companies(languages, companies)

df.to_csv("dataset.csv")

# removing sentences with no tag: reduces the dataset size from 25929 sentences to 2682.
print(len(df.index))
df = df[df.tag != ("",)]
print(len(df.index))

# splits: train: 20 (80%) first companies in alphabetic order, validation: 2 (8%) (Tumblr and Uber), test: 3 (12%) (Weebly, Yelp, Zynga)
validation_companies = ["Tumblr", "Uber"]
test_companies = ["Weebly", "Yelp", "Zynga"]
train_companies = sorted(list(set(companies) - set(validation_companies) - set(test_companies)))

# create splits
train = df[df.company.isin(train_companies)]
validation = df[df.company.isin(validation_companies)]
test = df[df.company.isin(test_companies)]


# save splits
def save_splits_to_jsonl(config_name):
    # save to jsonl files for huggingface
    if config_name: os.makedirs(config_name, exist_ok=True)
    train.to_json(os.path.join(config_name, "train.jsonl"), lines=True, orient="records", force_ascii=False)
    validation.to_json(os.path.join(config_name, "validation.jsonl"), lines=True, orient="records", force_ascii=False)
    test.to_json(os.path.join(config_name, "test.jsonl"), lines=True, orient="records", force_ascii=False)


save_splits_to_jsonl("")

# make labels nicer again
train.tag = train.tag.apply(lambda x: " ".join(list(x)))
validation.tag = validation.tag.apply(lambda x: " ".join(list(x)))
test.tag = test.tag.apply(lambda x: " ".join(list(x)))


def print_split_table(train, validation, test, label_name):
    train_counts = train[label_name].value_counts().to_frame().rename(columns={label_name: "train"})
    validation_counts = validation[label_name].value_counts().to_frame().rename(columns={label_name: "validation"})
    test_counts = test[label_name].value_counts().to_frame().rename(columns={label_name: "test"})

    table = train_counts.join(validation_counts)
    table = table.join(test_counts)
    table[label_name] = table.index
    total_row = {label_name: "total",
                 "train": len(train.index),
                 "validation": len(validation.index),
                 "test": len(test.index)}
    table = table.append(total_row, ignore_index=True)
    table = table[[label_name, "train", "validation", "test"]]  # reorder columns
    print(table.to_markdown(index=False))


print_split_table(train, validation, test, "tag")
