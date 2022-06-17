import pandas as pd
import requests
import os
from pathlib import Path
import os
from tqdm._tqdm_notebook import tqdm_notebook


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

RulingBR_complete = pd.read_json('RulingBR/rulingbr-master/complete.json',lines=True)

RulingBR_complete['text']=RulingBR_complete['ementa']+' '+RulingBR_complete['acordao']+' '+RulingBR_complete['relatorio']+' '+RulingBR_complete['voto']
RulingBR_complete['id'] = RulingBR_complete.index
RulingBR_complete['type'] = 'caselaw' # caselaw = 'Rechtssprechung'; because these are decisions from judges
RulingBR_complete['language'] = 'Brazilian Portuguese'
RulingBR_complete['jurisdiction'] = 'Brazil' # Because of the url the data was scraped from: https://www.stf.jus.br/
RulingBR_complete['title'] = ''
RulingBR_complete['date'] = ''
RulingBR_complete['url'] = ''
RulingBR_complete['metadata'] = ''

print('Total number of documents: ', RulingBR_complete.shape[0])

RulingBR_complete.to_json('Portuguese_Brazil_RulingBR.jsonl',force_ascii=False,orient='records', lines=True,indent=2)

