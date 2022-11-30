import pandas as pd
from tqdm import tqdm
from datasets import load_dataset, get_dataset_config_names
from datasets import disable_caching

tqdm.pandas()

#disable_caching()


def get_size(dataset_name, config):
    config_dataset = load_dataset(dataset_name, config)
    splits = list(config_dataset.keys())
    final_size = 0
    for split in splits:
        try:
            size = round(config_dataset[split].size_in_bytes/1000000,0)
            final_size+=size
        except Exception as e:
            print('Stop!')
            print(e)
            print(dataset_name, config)
            break
    return final_size

def apply_changes(dataset_name, file_path):
    if dataset_name=='pile-of-law/pile-of-law':
        df = pd.read_csv(file_path)

        df['Size (MB)']=df.config.progress_apply(lambda config: get_size(dataset_name,config))

        #df['Language']=df.config.apply(lambda x: x.split('_')[0])   
        #df['Source']=df.config.apply(lambda x: x.split('_')[1])

        df.rename(columns = {"config":"Source"}, inplace = True)

        df_restructured = df[['Source','Size (MB)','Tokens','Documents','Tokens/Document']]
        df_restructured = df_restructured.sort_values(['Source'], ascending=True)

        df_restructured.to_json(file_path[:-4]+'_edited.json',orient="records",lines=True,force_ascii=False)
        df_restructured.to_csv(file_path[:-4]+'_edited.csv',index=False)
    else:
        df = pd.read_csv(file_path)

        df['Size (MB)']=df.config.progress_apply(lambda config: get_size(dataset_name,config))

        df['Language']=df.config.apply(lambda x: x.split('_')[0])   
        df['Source']=df.config.apply(lambda x: x.split('_')[1])

        df_restructured = df[['Language','Source','Size (MB)','Tokens','Documents','Tokens/Document']]
        df_restructured = df_restructured.sort_values(['Language','Source'], ascending=True)

        df_restructured.to_json(file_path[:-4]+'_edited.json',orient="records",lines=True,force_ascii=False)
        df_restructured.to_csv(file_path[:-4]+'_edited.csv',index=False)


if __name__ == '__main__':
    
    file_path = 'Finished/results_of_joelito_Multi_Legal_Pile.csv'
    dataset_name = 'joelito/Multi_Legal_Pile'

    apply_changes(file_path=file_path, dataset_name=dataset_name)


