from datasets import load_dataset

from utils import save_and_compress

'''
    URL: https://www.kaggle.com/datasets/eliasjacob/brcad5?resource=download&select=language_modeling_texts.parquet
'''

dataset = load_dataset("parquet", data_files=f"language_modeling_texts.parquet",
                       split="train")
dataset = dataset.remove_columns(["__index_level_0__"])
print(dataset[0])

save_and_compress(dataset, 'CRETA')
