from datasets import load_dataset

from utils import save_and_compress

'''
URL: https://www.kaggle.com/datasets/eliasjacob/brcad5?resource=download&select=language_modeling_texts.parquet
'''

dataset = load_dataset("parquet", data_files=f"language_modeling_texts.parquet",
                       split="train")
dataset = dataset.remove_columns(["__index_level_0__", "case_number"])

dataset = dataset.rename_column("full_text_first_instance_court_ruling", "text")
dataset = dataset.add_column("type", ["caselaw"] * len(dataset))
dataset = dataset.add_column("jurisdiction", ["Brazil"] * len(dataset))
dataset = dataset.add_column("language", ["pt"] * len(dataset))

print(dataset[0])

save_and_compress(dataset, 'CRETA')
