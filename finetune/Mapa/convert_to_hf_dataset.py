import os
from glob import glob
from pathlib import Path

import numpy as np
import pandas as pd

from web_anno_tsv import open_web_anno_tsv
from web_anno_tsv.web_anno_tsv import ReadException, Annotation

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)

annotation_labels = {'ADDRESS': ['building', 'city', 'country', 'place', 'postcode', 'street', 'territory'],
                     'AMOUNT': ['unit', 'value'],
                     'DATE': ['year', 'standard abbreviation', 'month', 'day of the week', 'day', 'calender event'],
                     'PERSON': ['age', 'email', 'ethnic category', 'family name', 'financial', 'given name – female',
                                'given name – male',
                                'health insurance number', 'id document number', 'initial name', 'marital status',
                                'medical record number',
                                'nationality', 'profession', 'role', 'social security number', 'title', 'url'],
                     'ORGANISATION': [],
                     'TIME': [],
                     'VEHICLE': ['build year', 'colour', 'license plate number', 'model', 'type']}

# make all coarse_grained upper case and all fine_grained lower case
annotation_labels = {key.upper(): [label.lower() for label in labels] for key, labels in annotation_labels.items()}
print(annotation_labels)

base_path = Path("extracted")

# TODO future work can add these datasets too to make it larger
special_paths = {
    "EL": ["EL/ANNOTATED_DATA/LEGAL/AREIOSPAGOS1/annotated/full_dataset"],
    "EN": ["EN/ANNOTATED_DATA/ADMINISTRATIVE-LEGAL/annotated/full_dataset"],
    "FR": ["FR/ANNOTATED_DATA/LEGAL/COUR_CASSATION1/annotated/full_dataset/Civil",
           "FR/ANNOTATED_DATA/LEGAL/COUR_CASSATION1/annotated/full_dataset/Commercial",
           "FR/ANNOTATED_DATA/LEGAL/COUR_CASSATION1/annotated/full_dataset/Criminal",
           "FR/ANNOTATED_DATA/LEGAL/COUR_CASSATION2/annotated/full_dataset",
           "FR/ANNOTATED_DATA/MEDICAL/CAS1/annotated/full_dataset"],
    "IT": ["IT/ANNOTATED_DATA/Corte_Suprema_di_Cassazione/annotated"],
    "MT": ["MT/ANNOTATED_DATA/ADMINISTRATIVE/annotated/full_dataset",
           "MT/ANNOTATED_DATA/GENERAL_NEWS/News_1/annotated/full_dataset",
           "MT/ANNOTATED_DATA/LEGAL/Jurisprudence_1/annotated/full_dataset"],
}


def get_path(language):
    return base_path / language / "ANNOTATED_DATA/EUR_LEX/annotated/full_dataset"


def get_coarse_grained_for_fine_grained(label):
    for coarse_grained, fine_grained_set in annotation_labels.items():
        if label in fine_grained_set:
            return coarse_grained
    return None  # raise ValueError(f"Did not find fine_grained label {label}")


def is_fine_grained(label):
    for coarse_grained, fine_grained_set in annotation_labels.items():
        if label.lower() in fine_grained_set:
            return True
    return False


def is_coarse_grained(label):
    return label.upper() in annotation_labels.keys()


class HashableAnnotation(Annotation):
    def __init__(self, annotation):
        super()
        self.label = annotation.label
        self.start = annotation.start
        self.stop = annotation.stop
        self.text = annotation.text

    def __eq__(self, other):
        return self.label == other.label and self.start == other.start and self.stop == other.stop and self.text == other.text

    def __hash__(self):
        return hash(('label', self.label, 'start', self.start, 'stop', self.stop, 'text', self.text))


def get_token_annotations(token, annotations):
    annotations = list(dict.fromkeys([HashableAnnotation(ann) for ann in annotations]))  # remove duplicate annotations
    coarse_grained = "O"
    fine_grained = "o"
    for annotation in annotations:
        label = annotation.label
        # if token.start == annotation.start and token.stop == annotation.stop:  # fine_grained annotation
        if token.start >= annotation.start and token.stop <= annotation.stop:  # course_grained annotation
            # we don't support multilabel annotations for each token for simplicity.
            # So when a token already has an annotation for either coarse or fine grained, we don't assign new ones.
            if coarse_grained != "O" and is_coarse_grained(label):
                coarse_grained = label
            elif fine_grained != "o" and is_fine_grained(label):
                # some DATE are mislabeled as day but it is hard to correct this. So we ignore it
                fine_grained = label

    return coarse_grained.upper(), fine_grained.lower()


def get_annotated_sentence(result_sentence, sentence):
    result_sentence["tokens"] = []
    result_sentence["coarse_grained"] = []
    result_sentence["fine_grained"] = []
    for k, token in enumerate(sentence.tokens):
        coarse_grained, fine_grained = get_token_annotations(token, sentence.annotations)
        token = token.text.replace(u'\xa0', u' ').strip()  # replace non-breaking spaces
        if token:  # remove empty tokens (only consisted of whitespace before
            result_sentence["tokens"].append(token)
            result_sentence["coarse_grained"].append(coarse_grained)
            result_sentence["fine_grained"].append(fine_grained)
    return result_sentence


languages = sorted([Path(file).stem for file in glob(str(base_path / "*"))])


def parse_files(language):
    data_path = get_path(language.upper())
    result_sentences = []
    not_parsable_files = 0
    file_names = sorted(list(glob(str(data_path / "*.tsv"))))
    for file in file_names:
        try:
            with open_web_anno_tsv(file) as f:
                for i, sentence in enumerate(f):
                    result_sentence = {"language": language, "type": "EUR-LEX",
                                       "file_name": Path(file).stem, "sentence_number": i}
                    result_sentence = get_annotated_sentence(result_sentence, sentence)
                    result_sentences.append(result_sentence)
            print(f"Successfully parsed file {file}")
        except ReadException as e:
            print(f"Could not parse file {file}")
            not_parsable_files += 1
    print("Not parsable files: ", not_parsable_files)
    return pd.DataFrame(result_sentences), not_parsable_files


stats = []
train_dfs, validation_dfs, test_dfs = [], [], []
for language in languages:
    language = language.lower()
    print(f"Parsing language {language}")
    df, not_parsable_files = parse_files(language)
    file_names = df.file_name.unique()

    # split by file_name
    num_fn = len(file_names)
    train_fn, validation_fn, test_fn = np.split(np.array(file_names), [int(.8 * num_fn), int(.9 * num_fn)])

    lang_train = df[df.file_name.isin(train_fn)]
    lang_validation = df[df.file_name.isin(validation_fn)]
    lang_test = df[df.file_name.isin(test_fn)]

    train_dfs.append(lang_train)
    validation_dfs.append(lang_validation)
    test_dfs.append(lang_test)

    lang_stats = {"language": language}

    lang_stats["# train files"] = len(train_fn)
    lang_stats["# validation files"] = len(validation_fn)
    lang_stats["# test files"] = len(test_fn)

    lang_stats["# train sentences"] = len(lang_train.index)
    lang_stats["# validation sentences"] = len(lang_validation.index)
    lang_stats["# test sentences"] = len(lang_test.index)

    stats.append(lang_stats)

stat_df = pd.DataFrame(stats)
print(stat_df.to_markdown(index=False))

train = pd.concat(train_dfs)
validation = pd.concat(validation_dfs)
test = pd.concat(test_dfs)

# save splits
def save_splits_to_jsonl(config_name):
    # save to jsonl files for huggingface
    if config_name: os.makedirs(config_name, exist_ok=True)
    train.to_json(os.path.join(config_name, "train.jsonl"), lines=True, orient="records", force_ascii=False)
    validation.to_json(os.path.join(config_name, "validation.jsonl"), lines=True, orient="records", force_ascii=False)
    test.to_json(os.path.join(config_name, "test.jsonl"), lines=True, orient="records", force_ascii=False)


save_splits_to_jsonl("")
