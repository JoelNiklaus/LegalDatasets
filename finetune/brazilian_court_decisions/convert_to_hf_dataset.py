import os

import numpy as np
import pandas as pd

"""
Dataset url: https://github.com/lagefreitas/predicting-brazilian-court-decisions/blob/main/dataset.zip
Paper url: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9044329/

There are no splits available ==> Make random split ourselves

"""

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)

df = pd.read_csv("dataset.csv", sep="<=>")

# remove strange " characters sometimes occurring in the beginning and at the end of a line
df.ementa_filepath = df.ementa_filepath.str.replace('^"', '')
df.decision_unanimity = df.decision_unanimity.str.replace('"$', '')

# removing process_type and judgment_date, since they are the same everywhere (-)
# decisions only contains 'None', nan and '-2'
# ementa_filepath refers to the name of file in the filesystem that we created when we scraped the data from the Court. It is temporary data and can be removed
# decision_description = ementa_text - decision_text - decision_unanimity_text
df = df.drop(['process_type', 'judgment_date', 'decisions', 'ementa_filepath'], axis=1)

# some rows are somehow not read correctly. With this, we can filter them
df = df[df.decision_text.str.len() > 1]

# rename "-2" to more descriptive name ==> -2 means, that they were not able to determine it
df.decision_unanimity = df.decision_unanimity.replace('-2', 'not_determined')

# rename cols for more clarity
df = df.rename(columns={"decision_unanimity": "unanimity_label"})
df = df.rename(columns={"decision_unanimity_text": "unanimity_text"})
df = df.rename(columns={"decision_text": "judgment_text"})
df = df.rename(columns={"decision_label": "judgment_label"})

# drop any duplicates: removes the size from 9608 to 4820 entries
print(len(df.index))
df = df.drop_duplicates()
print(len(df.index))

df.to_csv("dataset_processed.csv")

# perform random split 80% train (7686), 10% validation (961), 10% test (961)
train, validation, test = np.split(df.sample(frac=1, random_state=42), [int(.8 * len(df)), int(.9 * len(df))])

def save_splits_to_jsonl(config_name):
    # save to jsonl files for huggingface
    os.makedirs(config_name, exist_ok=True)
    train.to_json(config_name + "/train.jsonl", lines=True, orient="records", force_ascii=False)
    validation.to_json(config_name + "/validation.jsonl", lines=True, orient="records", force_ascii=False)
    test.to_json(config_name + "/test.jsonl", lines=True, orient="records", force_ascii=False)


# print label statistics for judgment config
print(train.judgment_label.value_counts())
print(validation.judgment_label.value_counts())
print(test.judgment_label.value_counts())

save_splits_to_jsonl("judgment")

# create second config by filtering out rows with unanimity label == not_determined, while keeping the same splits
train = train[train.unanimity_label != "not_determined"]
validation = validation[validation.unanimity_label != "not_determined"]
test = test[test.unanimity_label != "not_determined"]

print(train.unanimity_label.value_counts())
print(validation.unanimity_label.value_counts())
print(test.unanimity_label.value_counts())

save_splits_to_jsonl("unanimity")
