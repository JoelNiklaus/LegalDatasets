import glob
import os
from pathlib import Path

import pandas as pd

data_path = Path("corpus_NLLP2021")
languages = ["de", "en", "it", "pl"]
clause_topics = ["a", "ch", "cr", "j", "law", "ltd", "ter", "use", "pinc"]
unfairness_levels = {1: "clearly_fair", 2: "potentially_unfair", 3: "clearly_unfair", -1: "untagged"}

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
            sentences = read_lines(get_file_name("sentences", language, company))
            assert len(tags) == len(sentences), "The number of tags is not equal to the number of sentences"
            for i in range(len(sentences)):
                topics = [tag[:-1] for tag in tags[i].split(" ")] if tags[i] else []  # getting only the topic
                levels = [int(tag[-1:]) for tag in tags[i].split(" ")] if tags[i] else []  # getting only the level
                levels = list(set(levels))  # remove any duplicates
                row = {"language": language, "company": company, "sentence": sentences[i]}
                for topic in clause_topics:
                    row[topic] = True if topic in topics else False
                # assign "untagged" if not annotated (levels empty) or multiple different levels present
                if not levels or len(levels) > 1:
                    level = -1
                else:  # there is exactly one level
                    level = levels[0]
                    assert level in [1, 2, 3]
                row["unfairness_level"] = unfairness_levels[level]

                data.append(row)
    return pd.DataFrame.from_records(data)


df = read_companies(languages, companies)

df.to_csv("dataset.csv")

# not removing sentences with no tag ==> detecting whether a tag at all applies is part of the task
# print(len(df.index))
# df = df[df.tag != ("",)]
# print(len(df.index))

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


def print_split_table_single_label(train, validation, test, label_name):
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


save_splits_to_jsonl("clause_topics")

print_split_table_multi_label({"train": train, "validation": validation, "test": test}, clause_topics)

# remove all rows that don't have a fairness_level attached
train = train[train.unfairness_level != "untagged"]
validation = validation[validation.unfairness_level != "untagged"]
test = test[test.unfairness_level != "untagged"]

save_splits_to_jsonl("unfairness_levels")

print_split_table_single_label(train, validation, test, "unfairness_level")
