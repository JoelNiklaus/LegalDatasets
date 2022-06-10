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

# create a summary jsonl file
dataset_filename = "dataset.jsonl"
if not Path(dataset_filename).exists():
    with open(dataset_filename, "a") as dataset_file:
        for filename in glob("annotated_corpus/*.json"):
            # we need to do this charade, because some jsons are formatted differently than others
            json_text = Path(filename).read_text()
            json_obj = json.loads(json_text)
            new_dict = {}
            new_dict.update(json_obj["meta"])
            new_dict.update(json_obj["decision_text"])
            #print("tenor", len(new_dict["tenor"][0]))
            #print("legal_facts", len(new_dict["legal_facts"][0]))
            #print("decision_reasons", len(new_dict["decision_reasons"][0]))
            dataset_file.write(json.dumps(new_dict) + "\n")
else:
    print(f"{dataset_filename} already exists. Please delete it to re-aggregate it.")

df = pd.read_json(dataset_filename, lines=True)

counter = 10
for i in range(200):
    for paragraph in df.iloc[i].decision_reasons:
        for sentence in paragraph:
            if len(sentence[0]) < 15:
                counter += 1
                print(sentence)
print(counter)
# TODO think about removing very short sentences or concatenating them to the next one if the label is the same

# perform random split 80% train (7686), 10% validation (961), 10% test (961)
train, validation, test = np.split(df.sample(frac=1, random_state=42), [int(.8 * len(df)), int(.9 * len(df))])

# save to jsonl files for huggingface
train.to_json("train.jsonl", lines=True, orient="records")
validation.to_json("validation.jsonl", lines=True, orient="records")
test.to_json("test.jsonl", lines=True, orient="records")
