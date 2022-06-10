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

df.to_csv("dataset_processed.csv")

# perform random split 80% train (7686), 10% validation (961), 10% test (961)
train, validation, test = np.split(df.sample(frac=1, random_state=42), [int(.8 * len(df)), int(.9 * len(df))])

print(train.decision_label.value_counts())
print(validation.decision_label.value_counts())
print(test.decision_label.value_counts())

print(train.decision_unanimity.value_counts())
print(validation.decision_unanimity.value_counts())
print(test.decision_unanimity.value_counts())


# save to jsonl files for huggingface
train.to_json("train.jsonl", lines=True, orient="records")
validation.to_json("validation.jsonl", lines=True, orient="records")
test.to_json("test.jsonl", lines=True, orient="records")
