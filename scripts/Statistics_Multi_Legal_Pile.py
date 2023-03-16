#!/usr/bin/env python
# coding: utf-8


from transformers import AutoTokenizer
import pandas as pd
from datasets import load_dataset, get_dataset_config_names
import re
from traceback import print_exc
import os
import argparse

tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-base")


def get_already_processed_configs(output_file: str):
    df = pd.read_csv(output_file)
    configs = df.config.tolist()
    return configs


def get_overview(dataset_name, config, filename=None, repo_data_only=True, compute_tokens=False):
    if filename is None:
        filename = re.sub(r'\/', '_', dataset_name)
    else:
        filename = re.sub(r'\/', '_', filename)
    file_name = 'results_of_' + filename + '.csv'

    if os.path.isfile(file_name):
        configs = get_already_processed_configs(file_name)
    else:
        configs = []

    if config not in configs:

        results_scattered = list()

        for split in ["train", "validation", "test"]:
            try:
                dataset = load_dataset(dataset_name, config, split=split, streaming=True)
                if compute_tokens:
                    dataset = dataset.map(
                        lambda examples: tokenizer(examples["text"], add_special_tokens=False, return_length=True),
                        batched=True, batch_size=1000)
                dataset = dataset.map(lambda examples: {"length_words": len(examples["text"].split())})
                result_dict = dict()
                Tokens, Words, Documents = 0, 0, 0
                for document in dataset:
                    if compute_tokens:
                        Tokens += document['length']
                    Words += document['length_words']
                    Documents += 1

                result_dict['config'] = config
                if compute_tokens:
                    result_dict['Tokens'] = Tokens
                result_dict['Words'] = Words
                result_dict['Documents'] = Documents
                results_scattered.append(result_dict)
            except Exception as e:
                print(print_exc())
                print('No ', split, ' in ', dataset_name, ' ', config)

        results_scattered = pd.DataFrame(results_scattered)

        final_result_dict = dict()
        final_result_dict["config"] = config
        if compute_tokens:
            final_result_dict["Tokens"] = results_scattered.Tokens.sum()
        final_result_dict["Words"] = results_scattered.Words.sum()
        final_result_dict["Documents"] = results_scattered.Documents.sum()
        try:
            if compute_tokens:
                final_result_dict["Tokens/Document"] = round(
                    int(final_result_dict["Tokens"] / final_result_dict["Documents"]), 0)
            final_result_dict["Words/Document"] = round(
                int(final_result_dict["Words"] / final_result_dict["Documents"]), 0)
        except:
            if compute_tokens:
                final_result_dict["Tokens/Document"] = 0
            final_result_dict["Words/Document"] = 0

        if os.path.isfile(file_name):
            pd.DataFrame([final_result_dict]).to_csv(file_name, mode='a', header=False, index=False)
        else:
            pd.DataFrame([final_result_dict]).to_csv(file_name, index=False)

        return final_result_dict

    else:
        print('Config ', config, ' already processed. We will skip it.')


def create_overview(dataset_name, available_configs, filename=None):
    results = list()

    for config in available_configs:
        # TODO skip configs that have been computed already so that we can resume
        result_dict = get_overview(dataset_name, config, filename)
        results.append(result_dict)

    results_df = pd.DataFrame(results)

    if filename is None:
        filename = re.sub(r'\/', '_', dataset_name)

    with open('results_of_' + filename + '.md', 'w') as f:
        print(results_df.to_markdown(), file=f)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    # TODO also add individual sources of native multi_legal_pile data

    parser.add_argument('-dsn', '--dataset_names', help="Specify dataset name.",
                        default=['joelito/Multi_Legal_Pile', 'joelito/legal-mc4', 'joelito/eurlex_resources',
                                 'pile-of-law/pile-of-law', 'joelito/EU_Wikipedias',
                                 'joelito/MultiLegalPileWikipediaFiltered'])

    args = parser.parse_args()

    if type(args.dataset_names) == str:
        dataset_names = [args.dataset_names]
    else:
        dataset_names = args.dataset_names

    print(dataset_names)

    # dataset_names = ['joelito/Multi_Legal_Pile']
    iteration_dict = {dataset_name: get_dataset_config_names(dataset_name) for dataset_name in dataset_names}

    for dataset_name, configs in iteration_dict.items():
        print('Processing ', dataset_name)
        create_overview(dataset_name, configs)
