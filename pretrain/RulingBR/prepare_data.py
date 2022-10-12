import pandas as pd

from utils import save_and_compress

'''
    URL: https://github.com/diego-feijo/rulingbr
    Status: in progress

Important information

    The file contains these columns ['ementa', 'acordao', 'relatorio', 'voto']; the description of each column is given in the Github repository

    First, I wanted to choose to take the column voto because it contains, on average, most of the textual material
        Mean number of characters for ementa: 1094.7389626282595
        Mean number of characters for acordao: 397.94916690200506
        Mean number of characters for relatorio: 3530.7663560199567
        Mean number of characters for voto: 11316.868116351314

    But then I decided to combine each field into one text field

'''

df = pd.read_json('complete.json', lines=True)
print(df.head())

df['text'] = df['ementa'] + ' ' + df['acordao'] + ' ' + df[
    'relatorio'] + ' ' + df['voto']
df['id'] = df.index
df['type'] = 'caselaw'  # caselaw = 'Rechtssprechung'; because these are decisions from judges
df['language'] = 'pt'  # 'Brazilian Portuguese'
df['jurisdiction'] = 'Brazil'  # Because of the url the data was scraped from: https://www.stf.jus.br/

df = df[['type', 'language', 'jurisdiction', 'text']]


print(df.head())

print('Total number of documents: ', df.shape[0])

save_and_compress(df, 'RulingBR')
