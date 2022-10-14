import datasets
from datasets import load_dataset
from huggingface_hub.file_download import hf_hub_url

from utils import save_and_compress

"""
Legislation from Norway in no
"""
# These are the different doc types. Everything is legislation (based on our research)
legislation_types = ['lovdata_cd_odelsting_2005', 'lovdata_cd_somb_rundskriv_2005',
                     'lovdata_cd_sentrale_forskrifter_2005', 'lovdata_cd_lokaleforskrifter_2005',
                     'lovdata_cd_norgeslover_2005', 'lovdata_cd_rtv_rundskriv_2005',
                     'lovdata_cd_skatt_rundskriv_2005', 'lovdata_cd_rundskriv_lovavdeling_2005']


def get_ncc_url(filename):
    return hf_hub_url(repo_id="NbAiLab/NCC", filename=filename, repo_type="dataset")


data = []
for i in range(1, 47):
    train_file = get_ncc_url(f"data/train-shard-00{i:02d}-of-0046.json.gz")
    print(f"Processing {train_file}")
    train = load_dataset("json", data_files=train_file, split="train", use_auth_token=True)
    train = train.filter(lambda example: example['doc_type'].startswith('lovdata_cd'))
    data.append(train)

validation_file = get_ncc_url("data/validation-shard-0001-of-0001.json.gz")
validation = load_dataset("json", data_files=validation_file, split="train", use_auth_token=True)
validation = validation.filter(lambda example: example['doc_type'].startswith('lovdata_cd'))
data.append(validation)

legislation = datasets.concatenate_datasets(data)

legislation = legislation.add_column("type", ["legislation"] * len(legislation))
legislation = legislation.add_column("language", ["no"] * len(legislation))
legislation = legislation.add_column("jurisdiction", ["Norway"] * len(legislation))

cols_to_remove = ['id', 'doc_type', 'publish_year', 'lang_fasttext', 'lang_fasttext_conf']
legislation = legislation.remove_columns(cols_to_remove)

print(legislation)

save_and_compress(legislation, 'legislation_norway')
