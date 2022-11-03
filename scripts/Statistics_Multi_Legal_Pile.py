#!/usr/bin/env python
# coding: utf-8


from transformers import AutoTokenizer
import pandas as pd
from datasets import load_dataset, get_dataset_config_names
import re
from traceback import print_exc
import os

tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-base")


def get_overview(dataset_name, config):
    results_scattered = list()

    for split in ["train", "validation", "test"]:
        try:
            dataset = load_dataset(dataset_name, config, split=split, streaming=True)
            print(dataset)
            dataset = dataset.map(
                lambda examples: tokenizer(examples["text"], add_special_tokens=False, return_length=True),
                batched=True, batch_size=1000)
            result_dict = dict()
            Tokens = 0
            Documents = 0
            for batch in dataset:
                Tokens += batch['length']
                Documents += 1

            result_dict['config'] = config
            result_dict['Tokens'] = Tokens
            result_dict['Documents'] = Documents
            # result_dict['Words/Document'] = int(round(mean(dataset["length"]),0))
            results_scattered.append(result_dict)
        except Exception as e:
            print(print_exc())
            print('No ', split, 'in ', dataset_name, ' ', config)
            pass

    results_scattered = pd.DataFrame(results_scattered)

    final_result_dict = dict()
    final_result_dict["config"] = config
    final_result_dict["Tokens"] = results_scattered.Tokens.sum()
    final_result_dict["Documents"] = results_scattered.Documents.sum()
    final_result_dict["Words/Document"] = round(int(final_result_dict["Tokens"] / final_result_dict["Documents"]), 0)

    filename = re.sub(r'\/', '_', dataset_name)
    file_name = 'results_of_' + filename + '.csv'

    if os.path.isfile(file_name):
        pd.DataFrame([final_result_dict]).to_csv(file_name, mode='a', header=False, index=False)
    else:
        pd.DataFrame([final_result_dict]).to_csv(file_name, index=False)

    return final_result_dict


def create_overview(dataset_name, available_configs):
    results = list()

    for config in available_configs:
        result_dict = get_overview(dataset_name, config)
        results.append(result_dict)

    results_df = pd.DataFrame(results)

    filename = re.sub(r'\/', '_', dataset_name)

    with open('results_of_' + filename + '.md', 'w') as f:
        print(results_df.to_markdown(), file=f)


if __name__ == '__main__':
    # TODO also add individual sources of native multi_legal_pile data
    dataset_names = ['joelito/Multi_Legal_Pile', 'joelito/mc4_legal', 'joelito/eurlex_resources',
                     'pile-of-law/pile-of-law']
    iteration_dict = {dataset_name: get_dataset_config_names(dataset_name) for dataset_name in dataset_names}

    for dataset_name, config in iteration_dict.items():
        print('Processing ', dataset_name)
        create_overview(dataset_name, config)
