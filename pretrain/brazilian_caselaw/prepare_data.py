import json
import os

from tqdm import tqdm

from datasets import load_dataset

try:
    import lzma as xz
except ImportError:
    import pylzma as xz

"""
Caselaw from Brazil in pt: cjpg
"""

dataset = load_dataset("json", data_dir="cjpg/results_as_json", split="train")

dataset = dataset.rename_column("julgado", "text")
dataset = dataset.add_column("type", ["caselaw"] * len(dataset))
dataset = dataset.add_column("jurisdiction", ["Brazil"] * len(dataset))
dataset = dataset.add_column("language", ["pt"] * len(dataset))
dataset = dataset.remove_columns(['processo', 'pagina', 'hora_coleta', 'duplicado', 'classe', 'assunto',
                                  'magistrado', 'comarca', 'foro', 'vara', 'disponibilizacao', 'cd_doc'])
print(dataset[0])

MAX_FILE_SIZE = 2e9  # 2GB max file size


def get_output_file_name(output_file_idx):
    return f"cjpg.{output_file_idx}.jsonl.xz"


def open_new_file(output_file_idx):
    filename = get_output_file_name(output_file_idx)
    print(f"Writing to {filename}")
    return xz.open(filename, "wt")


output_file_idx = 0
file = open_new_file(output_file_idx)
for datapoint in tqdm(dataset):
    if os.path.getsize(get_output_file_name(output_file_idx)) > MAX_FILE_SIZE:
        file.close()
        output_file_idx += 1
        file = open_new_file(output_file_idx)
    file.write(json.dumps(datapoint) + "\n")
file.close()

# Upload stuff to mega
# megaput --config=/home/fdn-admin/mega.cnf --path=/Root --disable-previews "/home/fdn-admin/LegalDatasets/backup.zip"
