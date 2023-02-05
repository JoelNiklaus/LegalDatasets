# No chunks, one doc per line

# remove new lines, etc.
# create a corpus of min 200-400 GB ==> ~100B tokens
# max file size: 4GB because of huggingface
# validation set: ~100M tokens ==> 200-400MB

import json
import logging
import multiprocessing
import sys

import tqdm
import os
import re
from multiprocessing import Pool

from datasets import load_dataset
from tokenizers import normalizers

try:
    import lzma as xz
except ImportError:
    import pylzma as xz

root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)
logger = logging.getLogger(__name__)

_LANGUAGES = ['bg', 'cs', 'da', 'de', 'el', 'en', 'es', 'et', 'fi', 'fr', 'ga', 'hr',
              'hu', 'it', 'lt', 'lv', 'mt', 'nl', 'pl', 'pt', 'ro', 'sk', 'sl', 'sv']
_DOMAIN_TYPES = ['legislation', 'caselaw', 'contracts', 'other', 'mc4-legal' 'wikipedia']

custom_normalizer = normalizers.NFKD()

VALIDATION_SIZE = 1_000  # ~1MB per configuration ==> some low-resource configs will only have a validation file
MAX_FILE_SIZE = int(5e8)  # 500 MB per train file

data_dir = 'data'
os.makedirs(data_dir, exist_ok=True)


def preprocess_dataset(languages=None, domain_types=None):
    lang_type_datasets = []
    # set defaults if they are not set
    if languages is None:
        languages = _LANGUAGES
    if domain_types is None:
        domain_types = _DOMAIN_TYPES

    for LANG in languages:
        for DOMAIN_TYPE in domain_types:
            try:
                if DOMAIN_TYPE == 'wikipedia':
                    # get from EU_Wikipedias
                    dataset = load_dataset("joelito/EU_Wikipedias", date="20221120", language=LANG,
                                           split='train', streaming=True, use_auth_token=True)
                else:
                    # get from Multi_Legal_Pile
                    dataset = load_dataset("joelito/Multi_Legal_Pile", f'{LANG}_{DOMAIN_TYPE}',
                                           split='train', streaming=True, use_auth_token=True)
                dataset = dataset.shuffle(seed=42, buffer_size=10_000)
                logger.info(f'Found data for `{DOMAIN_TYPE}` in language `{LANG}`.')
            except:
                logger.info(f'There is no data for `{DOMAIN_TYPE}` in language `{LANG}`.')
                continue
            lang_type_datasets.append(dataset)
    return lang_type_datasets


def write_samples(dataset_number):
    dataset, dataset_name = dataset_number
    if len(dataset_name.split('_')) == 1:  # wikipedia
        language = dataset_name.split('.')[1]
        domain_type = "wikipedia"
        dataset_name = f"{language}_{domain_type}"  # reformat the config name so that we have wikipedia in the name
    else:
        language, domain_type = dataset_name.split('_')
    total_count, temp_count, all_samples, file_number = 0, 0, 0, 0
    filepath = get_filepath(dataset_name, 'validation', file_number)  # we save the first examples to the validation set
    out_file = open_file(filepath)
    logger.info(f'Processing for dataset {dataset_name} started!')
    # Read each document
    for sample in tqdm.tqdm(dataset):
        try:
            if "validation" in filepath and temp_count >= VALIDATION_SIZE:
                # if we are saving to eval, and we have enough samples in the eval set, switch to train
                logger.info(
                    f'Processing validation split in dataset {dataset_name} finished with {temp_count}/{all_samples}!')
                out_file.close()
                temp_count = 0
                filepath = get_filepath(dataset_name, 'train', file_number)
                out_file = open_file(filepath)
            if "train" in filepath and os.path.getsize(filepath) > MAX_FILE_SIZE:
                # if we are saving to train, and we reached the max size per file, switch to the next file
                logger.info(
                    f'Processing file {file_number} of train split in dataset {dataset_name} finished with {temp_count}/{all_samples}!')
                out_file.close()
                file_number += 1
                temp_count = 0
                filepath = get_filepath(dataset_name, 'train', file_number)
                out_file = open_file(filepath)

            text = normalize_text(sample['text'])
            # if the text is usable for pretraining, save it
            if is_text_usable(text):
                jurisdiction = sample.get('jurisdiction', "N/A")  # set defaults for wikipedia
                type = sample.get("type", "wikipedia")  # set defaults for wikipedia
                entry = {"language": sample["language"], "type": type, "jurisdiction": jurisdiction, "text": text}
                out_file.write(json.dumps(entry) + '\n')
                total_count += 1
                temp_count += 1
            all_samples += 1
        except:
            continue

    try:
        out_file.close()
    except:
        pass

    logger.info(f'Processing for dataset {dataset_name} finished with {total_count}/{all_samples}!')
    return


def is_text_usable(text):
    # Compute percentage of alphabetical characters in relation to full sequence length
    punctuation = '!\"#$%&\'()*+,\-\./:;<=>?@\[\\\]\^_`{\|}~'
    alpha_text = re.sub(rf'[{punctuation}\d]', '', text)  # remove numbers and punctuation
    alpha_percent = len(alpha_text) / len(text)
    # Compute total chunk length
    text_length = len(text.split())
    # Ignore sequences with more than 30% numbers or short sequences (less than 64 tokens)
    return alpha_percent > 0.7 and text_length > 64


def normalize_text(text):
    # Normalize the document
    text = custom_normalizer.normalize_str(text)
    # Replace multiple newline and whitespaces
    return re.sub(r'(\n )+', r'\n ', re.sub(r'( *[\n\r]+ *)+', r'\n ', re.sub(r'[\t ]+', r' ', text)))


def open_file(filepath):
    logger.info(f'Writing to file {filepath}')
    return xz.open(filepath, 'wt')


def get_filepath(dataset_name, split, file_number):
    return os.path.join(data_dir, f'{dataset_name}_{split}.{file_number}.jsonl.xz')


def clean_and_filter_documents(languages=None, domain_types=None):
    # Load all datasets across languages and types
    lang_type_datasets = preprocess_dataset(languages=languages, domain_types=domain_types)
    # also pass in dataset_name
    lang_type_datasets = [(dataset, dataset.config_name) for dataset in lang_type_datasets]
    logger.info(lang_type_datasets)

    # Launch pool to preprocess datasets in parallel
    max_num_processes = min(multiprocessing.cpu_count() - 4, len(lang_type_datasets))
    num_processes = max(max_num_processes, 1)
    logger.info(f'Launching a Pool with maximum {num_processes} processes...')
    with Pool(num_processes) as pool:
        pool.map(write_samples, lang_type_datasets)

    logger.info(f"Finished preparing legal data")


if __name__ == '__main__':
    # CURRENTLY RUNNING ON DGX STATION BFH
    """
    Run with 
    export PYTHONPATH=. && python prepare_legal_data.py | tee prepare_legal_data.log 
    """
    # clean_and_filter_documents(["mt"], ["caselaw"])  # for testing
    domains = ['legislation', 'caselaw', 'contracts', 'other', 'wikipedia']  # 'mc4-legal' is not ready yet
    clean_and_filter_documents(languages=None, domain_types=domains)

# Get locally
# def get_file(LANG, DOMAIN_TYPE, split, number):
#    base_folder = "data/mlm_dataset/chunks_512"
#    return f'{base_folder}/{LANG}_{DOMAIN_TYPE}_{split}_{number}.jsonl.xz'

# files = [get_file(LANG, DOMAIN_TYPE, 'train', i) for i in range(1, 5)]
# files = [f for f in files if os.path.exists(f)] # make sure the file actually exists
# dataset = load_dataset("json", data_files={'train': files}, split='train', streaming=True)

# TODO write dataset cards for chunked, eu wikipedia and filtered dataset
