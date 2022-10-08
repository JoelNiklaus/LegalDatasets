import pandas as pd

from utils import save_and_compress, select_and_clean

"""
Legislation from Belgium in fr and nl
"""

df = pd.read_json('2022_06_04__22_29ejustice.jsonl', lines=True)
# print(df.head())
# print(df.columns)
# print(df.Language.value_counts())
# print(df.Source.value_counts())
# print(df['Nature juridique'].value_counts())
# print(df['Département'].value_counts())
# print(df['Domaine juridique'].value_counts())

df = df.rename(columns={
    'Nature juridique': 'nature_juridique',
    'Département': 'departement',
    'Domaine juridique': 'legal_area',
    'Publication date': 'date',
    'Source': 'source',
    'Title': 'title',
    'Text': 'text',
    'Country': 'jurisdiction',
    'Number': 'number',
    'URL': 'url',
    'Language': 'language',
})
df['type'] = 'legislation'

df = select_and_clean(df)

save_and_compress(df, 'ejustice')
