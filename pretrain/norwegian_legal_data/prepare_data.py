import datasets
from datasets import load_dataset

from utils import save_and_compress

"""
Legislation from Norway 
"""
# These are the different doc types. Everything is legislation (based on our research)
legislation_types = ['lovdata_cd_odelsting_2005', 'lovdata_cd_somb_rundskriv_2005',
                     'lovdata_cd_sentrale_forskrifter_2005', 'lovdata_cd_lokaleforskrifter_2005',
                     'lovdata_cd_norgeslover_2005', 'lovdata_cd_rtv_rundskriv_2005',
                     'lovdata_cd_skatt_rundskriv_2005', 'lovdata_cd_rundskriv_lovavdeling_2005']

train = load_dataset('NbAiLab/NCC', split='train', use_auth_token=True)
train = train.filter(lambda example: example['doc_type'].startswith('lovdata_cd'))

validation = load_dataset('NbAiLab/NCC', split='validation', use_auth_token=True)
validation = validation.filter(lambda example: example['doc_type'].startswith('lovdata_cd'))

legislation = datasets.concatenate_datasets([train, validation])

legislation = legislation.add_column("type", ["legislation"] * len(legislation))
legislation = legislation.add_column("language", ["no"] * len(legislation))
legislation = legislation.add_column("jurisdiction", ["Norway"] * len(legislation))

print(legislation)

save_and_compress(legislation, 'legislation_norway')
