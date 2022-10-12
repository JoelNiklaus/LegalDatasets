import pandas as pd
import pycountry
from utils import save_and_compress, select_and_clean

"""
Case law and Legislation from many countries in many languages
"""


def get_country_name(code):
    try:
        return pycountry.countries.get(alpha_3=code).name
    except:
        print(code)
        return "N/A"


def prepare(type):
    df = pd.read_json(f'data/{type}.jsonl', lines=True, orient='records')

    if type == 'caselaw':
        df['jurisdiction'] = df.country
    else:  # with all other types, it is saved as an alpha_3 code
        df['jurisdiction'] = df.country.apply(get_country_name)

    df = df.rename(columns={'lang': 'language'})
    if type in ['constitution', 'law']:
        df['type'] = 'legislation'
    else:
        df['type'] = 'caselaw'
    print(df)

    df = select_and_clean(df)

    save_and_compress(df, type)


for type in ['constitution', 'caselaw', 'law', 'summary']:
    prepare(type)
