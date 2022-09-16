import os
from glob import glob
from pathlib import Path

from typing import List

import numpy as np
import pandas as pd

from spacy.lang.ro import Romanian

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)

base_path = Path("legalnero-data")
tokenizer = Romanian().tokenizer


def process_document(ann_file: str, text_file: Path, metadata: dict, tokenizer) -> List[dict]:
    """Processes one document (.ann file and .txt file) and returns a list of annotated sentences"""
    # read the ann file into a df
    ann_df = pd.read_csv(ann_file, sep="\t", header=None, names=["id", "entity_with_span", "entity_text"])
    sentences = open(text_file, 'r').readlines()

    # split into individual columns
    ann_df[["entity", "start", "end"]] = ann_df["entity_with_span"].str.split(" ", expand=True)
    ann_df.start = ann_df.start.astype(int)
    ann_df.end = ann_df.end.astype(int)

    not_found_entities = 0
    annotated_sentences = []
    current_start_index = 2  # somehow, here they start with 2 (who knows why)
    for sentence in sentences:
        ann_sent = {**metadata}

        doc = tokenizer(sentence)
        doc_start_index = current_start_index
        doc_end_index = current_start_index + len(sentence)
        current_start_index = doc_end_index + 1

        relevant_annotations = ann_df[(ann_df.start >= doc_start_index) & (ann_df.end <= doc_end_index)]
        for _, row in relevant_annotations.iterrows():
            sent_start_index = row["start"] - doc_start_index
            sent_end_index = row["end"] - doc_start_index
            char_span = doc.char_span(sent_start_index, sent_end_index, label=row["entity"], alignment_mode="expand")
            # ent_span = Span(doc, char_span.start, char_span.end, row["entity"])
            if char_span:
                doc.set_ents([char_span])
            else:
                not_found_entities += 1
                print(f"Could not find entity `{row['entity_text']}` in sentence `{sentence}`")

        ann_sent["words"] = [str(tok) for tok in doc]
        ann_sent["ner"] = [tok.ent_iob_ + "-" + tok.ent_type_ if tok.ent_type_ else "O" for tok in doc]

        annotated_sentences.append(ann_sent)
    if not_found_entities > 0:
        # NOTE: does not find entities only in 2 cases in total
        print(f"Did not find entities in {not_found_entities} cases")
    return annotated_sentences


def read_to_df():
    """Reads the different documents and saves metadata"""
    ann_files = glob(str(base_path / "ann_LEGAL_PER_LOC_ORG_TIME" / "*.ann"))
    sentences = []
    file_names = []
    for ann_file in ann_files:
        file_name = Path(ann_file).stem
        text_file = base_path / "text" / f"{file_name}.txt"
        file_names.append(file_name)
        metadata = {
            "file_name": file_name,
        }
        sentences.extend(process_document(ann_file, text_file, metadata, tokenizer))
    return pd.DataFrame(sentences), file_names


df, file_names = read_to_df()

# last word is either "\n" or "-----" ==> remove
df.words = df.words.apply(lambda x: x[:-1])
df.ner = df.ner.apply(lambda x: x[:-1])

# remove rows with containing only one word
df = df[df.words.map(len) > 1]

print(f"The final tagset (in IOB notation) is the following: `{list(df.ner.explode().unique())}`")

# split by file_name
num_fn = len(file_names)
train_fn, validation_fn, test_fn = np.split(np.array(file_names), [int(.8 * num_fn), int(.9 * num_fn)])

# Num file_names for each split: train (296), validation (37), test (37)
print(len(train_fn), len(validation_fn), len(test_fn))

train = df[df.file_name.isin(train_fn)]
validation = df[df.file_name.isin(validation_fn)]
test = df[df.file_name.isin(test_fn)]

# Num samples for each split: train (7552), validation (966), test (907)
print(len(train.index), len(validation.index), len(test.index))


# save splits
def save_splits_to_jsonl(config_name):
    # save to jsonl files for huggingface
    if config_name: os.makedirs(config_name, exist_ok=True)
    train.to_json(os.path.join(config_name, "train.jsonl"), lines=True, orient="records", force_ascii=False)
    validation.to_json(os.path.join(config_name, "validation.jsonl"), lines=True, orient="records", force_ascii=False)
    test.to_json(os.path.join(config_name, "test.jsonl"), lines=True, orient="records", force_ascii=False)


save_splits_to_jsonl("")
