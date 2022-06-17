import pandas as pd
import requests
import os
from pathlib import Path
import os
from tqdm.notebook import tqdm
from ast import literal_eval


tqdm.pandas()

'''
You need to request the dataset
URL: http://ailab.unb.br/victor/lrec2020/

'''

#Read train
victor_train_medium = pd.read_csv('VICTOR/train_medium.csv')
victor_train_small = pd.read_csv('VICTOR/train_small.csv')
victor_train = pd.concat([victor_train_small,victor_train_medium])

#Read validation
victor_validation_medium = pd.read_csv('VICTOR/validation_medium.csv')
victor_validation_small = pd.read_csv('VICTOR/validation_small.csv')
victor_validation = pd.concat([victor_validation_small,victor_validation_medium])

#Read test
victor_test_medium = pd.read_csv('VICTOR/test_medium.csv')
victor_test_small = pd.read_csv('VICTOR/test_small.csv')
victor_test = pd.concat([victor_test_small,victor_test_medium])

victor_df = pd.concat([victor_train,victor_validation,victor_test])



victor_df = victor_df.drop_duplicates('body')

print('Number of documents to be processed: ',victor_df.shape[0])



def format_body(text):
    try:
        return list(literal_eval(text))[0]
    except Exception as e:
        #print(e)
        #print(text)
        return 'ERROR'

print('Converting document to json format:')
victor_df['body']=victor_df.body.progress_apply(lambda x: format_body(x))

#Remove all cases of body with value 'ERROR' from function format_body
victor_df = victor_df[victor_df.body!='ERROR']

victor_df.reset_index(inplace=True)


doc_type_translator_dic = dict()
doc_type_translator_dic['outros']='other'
doc_type_translator_dic['sentenca']='sentence/judgment'
doc_type_translator_dic['peticao_do_RE']="DEFENDANT'S petition"
doc_type_translator_dic['despacho_de_admissibilidade']='admissibility order'
doc_type_translator_dic['acordao_de_2_instancia']='2nd instance judgment'
doc_type_translator_dic['agravo_em_recurso_extraordinario']='grievance in extraordinary appeal'



victor_df['id']=victor_df.index
print('Translating the tags into English:')
victor_df['type']=victor_df.document_type.apply(lambda x: doc_type_translator_dic[x])
victor_df['language']='Brazilian Portuguese'
victor_df['jurisdiction']='Brazil'
victor_df['title']=''
victor_df['text']=victor_df.body
victor_df['date']=''
victor_df['url']=''
victor_df['meta']=''

for i, r in victor_df.iterrows():
    meta = dict()
    meta['process_id']=victor_df.at[i,'process_id']
    meta['themes']= victor_df.at[i,'themes']
    meta['file_name']= victor_df.at[i,'file_name']
    meta['pages']= victor_df.at[i,'pages']
    meta['document_type']= victor_df.at[i,'document_type']
    victor_df.at[i,'meta']=meta
    
for col in ['themes', 'process_id', 'file_name', 'document_type', 'pages', 'body']:
    del victor_df[col]
    

victor_df.to_json('Portuguese_Brazil_VICTOR.jsonl',force_ascii=False,orient='records', lines=True,indent=2)

