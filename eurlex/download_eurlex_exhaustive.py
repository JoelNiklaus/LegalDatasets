import os
import sys
from pathlib import Path

import requests
import glob
import logging
import re

from datetime import date


from bs4 import BeautifulSoup
from tqdm import tqdm
from pathos.multiprocessing import ProcessingPool as pool

sys.setrecursionlimit(100000)

global LOGGER

'''
Original Script by Ilias Chalkidis

IMPORTANT Disclaimer: For us this script did not work. This is why we used the R script to download the eurlex data

Types of documents in EUR-Lex
https://eur-lex.europa.eu/content/tools/TableOfSectors/types_of_documents_in_eurlex.html

CELEX numbers
https://eur-lex.europa.eu/content/tools/eur-lex-celex-infographic-A3.pdf
'''

'''
WARNING: The script does not download corrigenda
Run the script multiple times until no more files are downloaded
'''

DOWNLOAD_DIR = ''
Path(DOWNLOAD_DIR).mkdir(parents=True, exist_ok=True)

languages = [
    'BG', 'ES', 'CS', 'DA', 'DE', 'ET', 'EL', 'EN', 'FR', 'GA', 'HR', 'IT',
    'LV', 'LT', 'HU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK', 'SL', 'FI', 'SV'
]

sectors_dict = {
    'treaties': '1',
    'international_agreements': '2',
    'legal_acts': '3',
    'complementary_legislation': '4',
    'preparatory_documents': '5',
    'eu_case_law': '6',
    'national_transposition_measures': '7',
    'national_case_law': '8',
    'parliamentary_questions': '9',
    'efta_documents': 'E'
}

sectors_descriptors_dict = {
    'treaties': ['K', 'A', 'E', 'F', 'B', 'R', 'H', 'I', 'G', 'U', 'M', 'N', 'D', 'C', 'T', 'V', 'S', 'L', 'P', 'J',
                 'W', 'X', 'ME'],
    'international_agreements': ['A', 'D', 'P', 'X'],
    'legal_acts': ['E', 'F', 'R', 'L', 'D', 'S', 'M', 'J', 'B', 'K', 'O', 'H', 'A', 'G', 'C', 'Q', 'X', 'Y'],
    'complementary_legislation': ['A', 'D', 'X', 'Y', 'Z'],
    'preparatory_documents': [
        'AG', 'KG', 'IG', 'XG', 'PC', 'DC', 'JC', 'SC', 'EC', 'FC', 'GC', 'M', 'AT', 'AS', 'XC', 'AP', 'BP', 'IP', 'DP',
        'XP', 'AA', 'TA', 'SA', 'XA', 'AB', 'HB', 'XB', 'AE', 'IE', 'AC', 'XE', 'AR', 'IR', 'XR', 'AK', 'XK', 'XX'
    ],
    'eu_case_law': [
        'CJ', 'CO', 'CC', 'CS', 'CT', 'CV', 'CX', 'CD', 'CP', 'CN', 'CA', 'CB', 'CU', 'CG',
        'TJ', 'TO', 'TC', 'TT', 'TN', 'TA', 'TB', 'FJ', 'FO', 'FT', 'FN', 'FA', 'FB'
    ],
    'national_transposition_measures': ['L', 'F'],
    'national_case_law': [
        'BE', 'BG', 'CZ', 'DK', 'DE', 'EE', 'IE', 'EL', 'ES', 'FR', 'HR', 'IT', 'CY', 'LV', 'LT', 'LU',
        'HU', 'MT', 'NL', 'AT', 'PL', 'PT', 'RO', 'SI', 'SK', 'FI', 'SE', 'UK', 'CH', 'IS', 'NO', 'XX'
    ],
    'parliamentary_questions': ['E', 'H', 'O'],
    'efta_documents': ['A', 'C', 'G', 'J', 'P', 'X', 'O']
}

current_year = date.today().year

sectors_years_dict = {
    'treaties': (1951, current_year),
    'international_agreements': (1949, current_year),
    'legal_acts': (1952, current_year),
    'complementary_legislation': (1954, current_year),
    'preparatory_documents': (1957, current_year),
    'eu_case_law': (1954, current_year),
    'national_transposition_measures': (1942, current_year),
    'national_case_law': (1959, current_year),
    'parliamentary_questions': (1963, current_year),
    'efta_documents': (1992, current_year)
}


def set_logger(name='DOWNLOAD'):
    index = 0
    while True:
        index += 1
        log_filename = os.path.join(DOWNLOAD_DIR, f'EURLEX_{name}_{index}.log')
        if not os.path.isfile(log_filename):
            break

    logging.basicConfig(level=logging.INFO,
                        format='%(message)s',
                        datefmt='%m-%d %H:%M',
                        filename=log_filename,
                        filemode='w')

    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)

    # set a format which is simpler for console use
    formatter = logging.Formatter('%(message)s')

    # tell the handler to use this format
    console.setFormatter(formatter)

    # add the handler to the root logger
    # logging.getLogger('').addHandler(console)

    global LOGGER
    LOGGER = logging.getLogger(__name__)


def download_celex_id(celex_info):
    lang, sector, sector_descriptor, celex_id = celex_info
    url = f'https://eur-lex.europa.eu/legal-content/{lang}/TXT/HTML/?uri=CELEX:{celex_id}'
    filename = os.path.join(DOWNLOAD_DIR, lang, sector, sector_descriptor, re.sub('[/]', '_', celex_id) + '.txt')

    try:
        content = requests.get(url).text
        if 'Unfortunately this document cannot be displayed due to its size' in content:
            soup = BeautifulSoup(content, 'lxml')
            redirect_url = soup.find(lambda tag: tag.name == 'a' and 'Click here to view it.' in tag.text)['href']
            content = requests.get(redirect_url).text
            LOGGER.info(f'{celex_id:20} Unfortunately this document cannot be displayed due to its size\t {url}')

        if 'The requested document does not exist.' in content:
            LOGGER.info(f'{celex_id:20} The requested document does not exist.\t {url}')
        elif 'The request could not be satisfied.' in content or 'Request blocked.' in content or 'Generated by cloudfront (CloudFront)' in content:
            LOGGER.info(f'{celex_id:20} The request could not be satisfied.\t {url}')
        else:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(content)

            LOGGER.info(f'{celex_id:20} DONE')
    except Exception as error:
        LOGGER.info(f'{celex_id:20} ERROR {error}')


def main():
    set_logger()

    for lang in languages:
        os.makedirs(os.path.join(DOWNLOAD_DIR, lang), exist_ok=True)
        for sector in sectors_dict.keys():
            os.makedirs(os.path.join(DOWNLOAD_DIR, lang, sector), exist_ok=True)
            for sector_descriptor in sectors_descriptors_dict[sector]:
                os.makedirs(os.path.join(DOWNLOAD_DIR, lang, sector, sector_descriptor), exist_ok=True)
                eurlex_ids = []
                for year in range(sectors_years_dict[sector][1], sectors_years_dict[sector][0] - 1, -1):
                    for doc_id in range(0, 10000):
                        eurlex_ids.append(f'{sectors_dict[sector]}{year}{sector_descriptor}{doc_id:04d}')

                file_ids = [
                    re.sub('_', '/', f.split(os.sep)[-1].split('.')[0])
                    for f in glob.glob(os.path.join(DOWNLOAD_DIR, lang, sector, sector_descriptor, '*'))
                ]
                remaining = list(set(eurlex_ids) - set(file_ids))
                remaining = [(lang, sector, sector_descriptor, celex_id) for celex_id in remaining]

                msg = f'Starting Language: {lang} - Sector: {sector} - Descriptor: {sector_descriptor}'
                LOGGER.info(msg)
                print(msg)

                msg = f'Already downloaded: {len(file_ids)} - Trying: {len(remaining)} Celex IDs'
                LOGGER.info(msg)
                print(msg)

                calls = enumerate(pool(processes=1).imap(download_celex_id, remaining))
                for i, _ in tqdm(calls, total=len(remaining), ncols=100):
                    pass

                msg = f'End Language: {lang} - Sector: {sector} - Descriptor: {sector_descriptor}\n'
                LOGGER.info(msg)
                print(msg)


if __name__ == '__main__':
    main()
