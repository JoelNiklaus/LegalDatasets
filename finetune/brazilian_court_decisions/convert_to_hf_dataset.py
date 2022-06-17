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


def perform_original_preprocessing():
    # Original Preprocessing from: https://github.com/lagefreitas/predicting-brazilian-court-decisions/blob/main/predicting-brazilian-court-decisions.py#L81
    # Loading the labeled decisions
    data = pd.read_csv("dataset.csv", sep='<=>', header=0)
    print('data.shape=' + str(data.shape) + ' full data set')
    # Removing NA values
    data = data.dropna(subset=[data.columns[9]])  # decision_description
    data = data.dropna(subset=[data.columns[11]])  # decision_label
    print('data.shape=' + str(data.shape) + ' dropna')
    # Removing duplicated samples
    data = data.drop_duplicates(subset=[data.columns[1]])  # process_number
    print('data.shape=' + str(data.shape) + ' removed duplicated samples by process_number')
    data = data.drop_duplicates(subset=[data.columns[9]])  # decision_description
    print('data.shape=' + str(data.shape) + ' removed duplicated samples by decision_description')
    # Removing not relevant decision labels and decision not properly labeled
    data = data.query('decision_label != "conflito-competencia"')
    print('data.shape=' + str(data.shape) + ' removed decisions labeled as conflito-competencia')
    data = data.query('decision_label != "prejudicada"')
    print('data.shape=' + str(data.shape) + ' removed decisions labeled as prejudicada')
    data = data.query('decision_label != "not-cognized"')
    print('data.shape=' + str(data.shape) + ' removed decisions labeled as not-cognized')
    data_no = data.query('decision_label == "no"')
    print('data_no.shape=' + str(data_no.shape))
    data_yes = data.query('decision_label == "yes"')
    print('data_yes.shape=' + str(data_yes.shape))
    data_partial = data.query('decision_label == "partial"')
    print('data_partial.shape=' + str(data_partial.shape))
    # Merging decisions whose labels are yes, no, and partial to build the final data set
    data_merged = data_no.merge(data_yes, how='outer')
    data = data_merged.merge(data_partial, how='outer')
    print('data.shape=' + str(data.shape) + ' merged decisions whose labels are yes, no, and partial')
    # Removing decision_description and decision_labels whose values are -1 and -2
    indexNames = data[(data['decision_description'] == str(-1)) | (data['decision_description'] == str(-2)) | (
            data['decision_label'] == str(-1)) | (data['decision_label'] == str(-2))].index
    data.drop(indexNames, inplace=True)
    print('data.shape=' + str(data.shape) + ' removed -1 and -2 decision descriptions and labels')

    data.to_csv("dataset_processed_original.csv", index=False)


def perform_additional_processing():
    df = pd.read_csv("dataset_processed_original.csv")

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

    df.to_csv("dataset_processed_additional.csv", index=False)

    return df


perform_original_preprocessing()
df = perform_additional_processing()

# perform random split 80% train (3234), 10% validation (404), 10% test (405)
train, validation, test = np.split(df.sample(frac=1, random_state=42), [int(.8 * len(df)), int(.9 * len(df))])


def save_splits_to_jsonl(config_name):
    # save to jsonl files for huggingface
    if config_name: os.makedirs(config_name, exist_ok=True)
    train.to_json(os.path.join(config_name, "train.jsonl"), lines=True, orient="records", force_ascii=False)
    validation.to_json(os.path.join(config_name, "validation.jsonl"), lines=True, orient="records", force_ascii=False)
    test.to_json(os.path.join(config_name, "test.jsonl"), lines=True, orient="records", force_ascii=False)


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


save_splits_to_jsonl("judgment")

print_split_table_single_label(train, validation, test, "judgment_label")

# create second config by filtering out rows with unanimity label == not_determined, while keeping the same splits
train = train[train.unanimity_label != "not_determined"]
validation = validation[validation.unanimity_label != "not_determined"]
test = test[test.unanimity_label != "not_determined"]

print_split_table_single_label(train, validation, test, "unanimity_label")

# it is a very small dataset and very imbalanced (only very few not-unanimity labels)
save_splits_to_jsonl("unanimity")
