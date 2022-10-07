import pandas as pd
from pathlib import Path
from bs4 import BeautifulSoup
from tqdm import tqdm

from utils import save_and_compress


def format_file(file_path):
    result_dict = dict()

    content = open(file_path).read()
    soup = BeautifulSoup(content, 'xml')
    for x in soup.find_all('TITRE'):
        _title = x.text

    for x in soup.find_all('JURIDICTION'):
        _jurisdiction = x.text

    for x in soup.find_all('ID'):
        _id = x.text

    for x in soup.find_all('CONTENU'):
        _text = x.text

    for x in soup.find_all('DATE_DEC_ATT'):
        _date = x.text

    for x in soup.find_all('URL'):
        _url = x.text

    for x in soup.find_all('DEMANDEUR'):
        _claimant = x.text

    for x in soup.find_all('DEFENDEUR'):
        _defender = x.text

    for x in soup.find_all('SOMMAIRE'):
        _summary = x.text

    _type = 'caselaw'

    result_dict['title'] = _title
    result_dict['jurisdiction'] = _jurisdiction
    result_dict['id'] = _id
    result_dict['text'] = _text
    result_dict['date'] = _date
    result_dict['url'] = _url
    result_dict['type'] = _type

    result_dict['metadata'] = dict()
    result_dict['metadata']['claimant'] = _claimant
    result_dict['metadata']['defender'] = _defender
    result_dict['metadata']['summary'] = _summary

    return result_dict


# CASS Dataset
# https://github.com/euranova/CASS-dataset


# This does not work however
# url_dataset = 'ftp://echanges.dila.gouv.fr/CASS/Freemium_cass_global_20180315-170000.tar.gz'
# response = requests.get(url_dataset, stream=True)
# file = tarfile.open(fileobj=response.raw, mode="r|gz")
# file.extractall(path=".")


# Therefore, you can download the CASS dataset from here: https://echanges.dila.gouv.fr/OPENDATA/CASS/Freemium_cass_global_20220417-170000.tar.gz
path_to_cass = Path('./cass')

cass_files = [f for f in path_to_cass.glob('**/*') if f.is_file()]

cass_files = [format_file(f) for f in tqdm(cass_files) if str(f).endswith('xml')]
print(len(cass_files))

cass_files_df = pd.DataFrame(cass_files)

print('Number of records is: ', cass_files_df.shape)

save_and_compress(cass_files_df, 'cass')
