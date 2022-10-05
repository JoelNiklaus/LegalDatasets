import pandas as pd
import os
from pathlib import Path
import os
from tqdm import tqdm
from bs4 import BeautifulSoup

from pandarallel import pandarallel

pandarallel.initialize(progress_bar=True)

'''
You can download the corpus here: https://elrc-share.eu/repository/browse/marcell-slovak-legislative-subcorpus-v2/6bdee1d68c8311eb9c1a00155d0267063398d3f1a3af40e1b728468dcbd6efdd/
'''


def format_xml_file(path_to_file:str)->dict:

    try:
    
        content = open(path_to_file,'r').read()
        soup = BeautifulSoup(content,'lxml')
        
        item = dict()
        for x in soup.find_all('doc'):
            
            try:
                item['id']=x['id']
            except:
                item['id']=''
            try:
                item['date']=x['date']
            except:
                item['date']=''
            try:
                item['title']=x['title']
            except:
                item['title']=''
            try:
                item['url']=x['url']
            except:
                item['url']=''
            item['language']='Slovak'
            item['type']='legislation'
            item['jurisdiction']='Slovakia'
            item['metadata']=dict()
            try:
                item['metadata']['type']=x['type']
            except:
                item['metadata']['type']=''
            try:
                item['metadata']['entype']=x['entype']
            except:
                item['metadata']['entype']=''
            try:
                item['metadata']['keywords']=x['keywords']
            except:
                item['metadata']['keywords']=''
            try:
                item['metadata']['year']=x['year']
            except:
                item['metadata']['year']=''
            try:
                item['metadata']['position']=x['position']
            except:
                item['metadata']['position']=''
            try:
                item['metadata']['date_approved']=x['date_approved']
            except:
                item['metadata']['date_approved']=''
            try:
                item['metadata']['date_effect']=x['date_effect']
            except:
                item['metadata']['date_effect']=''
            try:
                item['metadata']['issuer']=x['issuer']
            except:
                item['metadata']['issuer']=''
            try:
                item['metadata']['eurovoc']=x['eurovoc']
            except:
                item['metadata']['eurovoc']=''
            try:
                item['metadata']['tld_score']=x['tld_score']
            except:
                item['metadata']['tld_score']=''
            try:
                item['metadata']['file']=x['file']
            except:
                item['metadata']['file']=''
            try:
                item['metadata']['nadpis']=x['nadpis']
            except:
                item['metadata']['nadpis']=''
            try:
                item['metadata']['number']=x['number']
            except:
                item['metadata']['number']=''
            try:
                item['metadata']['podnadpis']=x['podnadpis']
            except:
                item['metadata']['podnadpis']=''
            try:
                item['metadata']['predpisdatum']=x['predpisdatum']
            except:
                item['metadata']['predpisdatum']=''
            try:
                item['metadata']['predpistyp']=x['predpistyp']
            except:
                item['metadata']['predpistyp']=''
            try:
                item['metadata']['tokcount']=x['tokcount']
            except:
                item['metadata']['tokcount']=''
            try:
                item['metadata']['tokcountdd']=x['tokcountdd']
            except:
                item['metadata']['tokcountdd']=''

            
            item['text']=''
            

        for s in soup.find_all('s'):
            item['text']+=' '+s['text']
        
        print(str(path_to_file).split('/')[-1])
        return item
    except:
        print('Error')
        print(path_to_file)


if __name__=='__main__':

    path= './archive/' #Path to the downloaded folder

    path = Path(path)

    files = [f for f in path.glob('**/*') if f.is_file()]
    files = [x for x in files if str(x).endswith('xml')]
    print('Number of documents to be processed: ', len(files))

    '''
    df = pd.DataFrame(files,columns=['path'])
    df['item']=df.path.parallel_apply(lambda x: format_xml_file(x))

    items = df.item.tolist()
    df = pd.DataFrame(items)
    '''
    #
    files_as_dict = [format_xml_file(x) for x in tqdm(files)]
    df = pd.DataFrame(files_as_dict)

    df.to_json('Slovak_Slovakia_MARCELL_Slovak_legislative_subcorpus_v2.jsonl',force_ascii=False,orient='records', lines=True)