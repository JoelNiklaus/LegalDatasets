from glob import glob
from pathlib import Path

import json
import numpy as np
import pandas as pd

"""
Dataset url: https://zenodo.org/record/3936490/files/annotated_corpus.zip?download=1
Paper url: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9044329/

There are no splits available ==> Make random split ourselves

"""

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)


def analyze_dataset(df, num_characters_for_short_sentence=25):
    short_sentence = False
    counter = 0
    same_label_counter = 0
    other_number = 0
    num_one_paragraph_len = 0
    for i in range(200):
        for paragraph in df.iloc[i].decision_reasons:
            for sentence in paragraph:
                if short_sentence:
                    print("previous sentence was short: ", short_sentence)
                    print("current sentence label: ", sentence[1])
                    print("current paragraph: ", paragraph)
                    if sentence[1] == short_sentence[1]:
                        same_label_counter += 1

                if len(sentence[0]) < num_characters_for_short_sentence:
                    counter += 1
                    short_sentence = sentence
                    print()
                    print("short sentence: ", sentence)
                    print("short paragraph: ", paragraph)
                    if sentence[1] == 'other':
                        other_number += 1
                    if len(paragraph) == 1:
                        num_one_paragraph_len += 1
                else:
                    short_sentence = False

    print("num short sentences: ", counter)
    print("num short sentences containing the same label as the next one: ", same_label_counter)
    print("num short sentences containing 'other' as label: ", other_number)
    print("num short sentences where the paragraph contains only this one short sentence: ", num_one_paragraph_len)
    # ==> the label is only the same in very few cases
    # ==> the label is 'other' in the majority of cases, when it is not: it seems to be mislabeled
    # ==> think about removing them entirely
    # ==> we opted for not interfering in the content of the dataset


# create a summary jsonl file
dataset_filename = "dataset.jsonl"
if not Path(dataset_filename).exists():
    with open(dataset_filename, "a") as dataset_file:
        for filename in glob("annotated_corpus/*.json"):
            # we need to do this charade, because some jsons are formatted differently than others
            json_text = Path(filename).read_text()
            json_obj = json.loads(json_text)
            # make it less nested so that it is easier to read as df
            new_dict = {}
            new_dict.update(json_obj["meta"])
            new_dict.update(json_obj["decision_text"])
            dataset_file.write(json.dumps(new_dict) + "\n")
else:
    print(f"{dataset_filename} already exists. Please delete it to re-aggregate it.")

df = pd.read_json(dataset_filename, lines=True)

# Do splits before expanding the df so that entire decisions are in the splits and not samples from one decision are spread across splits
# perform random split 80% train (160 decisions), 10% validation (20 decisions), 10% test (20 decisions)
train, validation, test = np.split(df.sample(frac=1, random_state=42), [int(.8 * len(df)), int(.9 * len(df))])


def expand_df(df):
    """
    Expand the df so that each sentence has its own row and is its own sample
    :param df:
    :return:
    """
    rows = []
    for index, row in df.iterrows():
        for paragraph in row.decision_reasons:
            for sent_idx, sentence in enumerate(paragraph):
                new_row = {'file_number': row['file_number'], 'input_sentence': sentence[0], 'label': sentence[1]}
                # Discussion with lawyer yielded, that the paragraph as context is enough
                # take the sentences before
                new_row['context_before'] = paragraph[:sent_idx]
                # take the remaining sentences afterwards
                new_row['context_after'] = paragraph[sent_idx + 1:]
                rows.append(new_row)

    return pd.DataFrame.from_records(rows)


train = expand_df(train)
validation = expand_df(validation)
test = expand_df(test)

# Num samples for each split: train (19271), validation (2726), test (3078)
print(len(train.index), len(validation.index), len(test.index))

# save to jsonl files for huggingface
train.to_json("train.jsonl", lines=True, orient="records")
validation.to_json("validation.jsonl", lines=True, orient="records")
test.to_json("test.jsonl", lines=True, orient="records")

# save main df with meta information to file
# link to splits is given via file_number
df = df.drop(['decision_reasons'], axis=1)
df.to_json("meta.jsonl", lines=True, orient="records")
