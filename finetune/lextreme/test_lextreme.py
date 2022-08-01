import datasets
from datasets import load_dataset, get_dataset_config_names

dataset_name = "joelito/lextreme"
dataset_name = "lextreme.py"

configs = get_dataset_config_names(dataset_name)
print(configs)
for config in configs:
    lextreme_subset = load_dataset(dataset_name, config)
    splits = [datasets.Split.TRAIN, datasets.Split.VALIDATION, datasets.Split.TEST]
    assert [split in lextreme_subset for split in splits]
    assert [lextreme_subset[split].num_rows > 0 for split in splits]
    print(dataset_name, config)
    print(lextreme_subset)
