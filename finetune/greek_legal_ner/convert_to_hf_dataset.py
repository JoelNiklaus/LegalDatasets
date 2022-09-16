import os
from glob import glob
from pathlib import Path

from typing import List

import pandas as pd

from spacy.lang.el import Greek

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)

base_path = Path("DATASETS/ENTITY RECOGNITION")
tokenizer = Greek().tokenizer


# A and D are different government gazettes
# A is the general one, publishing standard legislation, and D is meant for legislation on urban planning and such things

def process_document(ann_file: str, text_file: Path, metadata: dict, tokenizer) -> List[dict]:
    """Processes one document (.ann file and .txt file) and returns a list of annotated sentences"""
    # read the ann file into a df
    ann_df = pd.read_csv(ann_file, sep="\t", header=None, names=["id", "entity_with_span", "entity_text"])
    sentences = [sent for sent in text_file.read_text().split("\n") if sent]  # remove empty sentences

    # split into individual columns
    ann_df[["entity", "start", "end"]] = ann_df["entity_with_span"].str.split(" ", expand=True)
    ann_df.start = ann_df.start.astype(int)
    ann_df.end = ann_df.end.astype(int)

    not_found_entities = 0
    annotated_sentences = []
    current_start_index = 0
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

    print(f"Did not find entities in {not_found_entities} cases")
    return annotated_sentences


def read_to_df(split):
    """Reads the different documents and saves metadata"""
    ann_files = glob(str(base_path / split / "ANN" / "*/*/*.ann"))
    sentences = []
    for ann_file in ann_files:
        path = Path(ann_file)
        year = path.parent.stem
        file_name = path.stem
        _, gazette, gazette_number, _, date = tuple(file_name.split(' '))
        text_file = base_path / split / "TXT" / f"{gazette}/{year}/{file_name}.txt"
        metadata = {
            "date": date,
            "gazette": gazette,
            # "gazette_number": gazette_number,
        }
        sentences.extend(process_document(ann_file, text_file, metadata, tokenizer))
    return pd.DataFrame(sentences)


splits = ["TRAIN", "VALIDATION", "TEST"]
train = read_to_df("TRAIN")
validation = read_to_df("VALIDATION")
test = read_to_df("TEST")

df = pd.concat([train, validation, test])
print(f"The final tagset (in IOB notation) is the following: `{list(df.ner.explode().unique())}`")


# save splits
def save_splits_to_jsonl(config_name):
    # save to jsonl files for huggingface
    if config_name: os.makedirs(config_name, exist_ok=True)
    train.to_json(os.path.join(config_name, "train.jsonl"), lines=True, orient="records", force_ascii=False)
    validation.to_json(os.path.join(config_name, "validation.jsonl"), lines=True, orient="records", force_ascii=False)
    test.to_json(os.path.join(config_name, "test.jsonl"), lines=True, orient="records", force_ascii=False)


save_splits_to_jsonl("")
