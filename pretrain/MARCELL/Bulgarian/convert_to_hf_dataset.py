import pandas as pd
from pathlib import Path
from tqdm import tqdm
from conllu import parse
from copy import deepcopy

'''
You can download the corpus here: https://elrc-share.eu/repository/browse/marcell-bulgarian-legislative-subcorpus-v2/946267fe8d8711eb9c1a00155d026706d2c9267e5cdf4d75b5f02168f01906c6/
'''


def format_conllup_file(path_to_file:str)->dict:

    try:

    
        content = open(path_to_file,'r').read()
        sentences = parse(content)
        metadata = dict(sentences[0].metadata)
        
        results = list()
        
        
        item = dict()
        item['id']=metadata['newdoc id']
        item['type']='legislation'
        item['language']='Bulgarian'
        item['jurisdiction']='Bulgarian'
        item['title']=metadata['title']
        item['date']=metadata['date']
        item['url']=''
        text = ' '
        for s in sentences:
            s_info = s.metadata
            text += ' '+s_info['text']
        
        item['text']=text


        #Delete metadata that we don't need
        metadata_final = deepcopy(metadata)
        for k in item.keys():
            if k!='type': #I will keep type because 'type' here means something else
                if k in metadata_final.keys():
                    del metadata_final[k]

        item['metadata']=metadata_final

        

        return item
    except Exception as e:
        print('Error for this file: ',path_to_file)
        print(e)

path= 'archive/bg-annotated' #Path to the downloaded folder

path = Path(path)

files = [f for f in path.glob('**/*') if f.is_file()]
files = [x for x in files if str(x).endswith('conllup')]
print('Number of documents to be processed: ', len(files))
files_as_dict = [format_conllup_file(x) for x in tqdm(files)]
files_as_dict = [x for x in tqdm(files_as_dict) if x is not None]
df = pd.DataFrame(files_as_dict)

df.to_json('Bulgarian_Bulgarian_MARCELL_Bulgarian_legislative_subcorpus_v2.jsonl',force_ascii=False,orient='records', lines=True)