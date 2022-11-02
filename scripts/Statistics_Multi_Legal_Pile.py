#!/usr/bin/env python
# coding: utf-8



from transformers import AutoTokenizer
import pandas as pd
from datasets import load_dataset, Dataset
from statistics import mean
import re


tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-base")



def get_overview(dataset_name, config):

    dataset = load_dataset(dataset_name, config)

    dataset_final = list()

    for split in ["train","validation","test"]:
        try:
            dataset_final.append(pd.DataFrame(dataset[split]))
        except:
            print('No ',split,'in ',dataset_name)
            pass
    
    dataset = pd.concat(dataset_final)
    dataset = Dataset.from_pandas(dataset)

    dataset = dataset.map(lambda examples: tokenizer(examples["text"],add_special_tokens=False, return_length=True), batched=True, batch_size=10000)

    result_dict = dict()
    result_dict['language__text_type'] = config
    result_dict['Tokens']= sum(dataset["length"])
    result_dict['Documents'] = dataset.shape[0]
    result_dict['Words/Document'] = int(round(mean(dataset["length"]),0))
    
    return result_dict



def create_overview(dataset_name, available_configs):
    
    results = list()
    
    for config in available_configs:
        result_dict = get_overview(dataset_name,config)
        results.append(result_dict)
        
    results_df = pd.DataFrame(results)

    filename = re.sub(r'\/','_',dataset_name)
    
    with open('results_of_'+filename+'.md','w') as f:
        print(results_df.to_markdown(), file=f)
    


iteration_dict = dict()
iteration_dict["joelito/Multi_Legal_Pile"]=['bg_caselaw', 'cs_caselaw', 'da_caselaw', 'de_caselaw', 'el_caselaw', 'en_caselaw', 'es_caselaw', 'et_caselaw', 'fi_caselaw', 'fr_caselaw', 'ga_caselaw', 'hr_caselaw', 'hu_caselaw', 'it_caselaw', 'lt_caselaw', 'lv_caselaw', 'mt_caselaw', 'nl_caselaw', 'pl_caselaw', 'pt_caselaw', 'ro_caselaw', 'sk_caselaw', 'sl_caselaw', 'sv_caselaw', 'all_caselaw', 'bg_contracts', 'cs_contracts', 'da_contracts', 'de_contracts', 'el_contracts', 'en_contracts', 'es_contracts', 'et_contracts', 'fi_contracts', 'fr_contracts', 'ga_contracts', 'hr_contracts', 'hu_contracts', 'it_contracts', 'lt_contracts', 'lv_contracts', 'mt_contracts', 'nl_contracts', 'pl_contracts', 'pt_contracts', 'ro_contracts', 'sk_contracts', 'sl_contracts', 'sv_contracts', 'all_contracts', 'bg_legislation', 'cs_legislation', 'da_legislation', 'de_legislation', 'el_legislation', 'en_legislation', 'es_legislation', 'et_legislation', 'fi_legislation', 'fr_legislation', 'ga_legislation', 'hr_legislation', 'hu_legislation', 'it_legislation', 'lt_legislation', 'lv_legislation', 'mt_legislation', 'nl_legislation', 'pl_legislation', 'pt_legislation', 'ro_legislation', 'sk_legislation', 'sl_legislation', 'sv_legislation', 'all_legislation', 'bg_other', 'cs_other', 'da_other', 'de_other', 'el_other', 'en_other', 'es_other', 'et_other', 'fi_other', 'fr_other', 'ga_other', 'hr_other', 'hu_other', 'it_other', 'lt_other', 'lv_other', 'mt_other', 'nl_other', 'pl_other', 'pt_other', 'ro_other', 'sk_other', 'sl_other', 'sv_other', 'all_other', 'bg_all', 'cs_all', 'da_all', 'de_all', 'el_all', 'en_all', 'es_all', 'et_all', 'fi_all', 'fr_all', 'ga_all', 'hr_all', 'hu_all', 'it_all', 'lt_all', 'lv_all', 'mt_all', 'nl_all', 'pl_all', 'pt_all', 'ro_all', 'sk_all', 'sl_all', 'sv_all', 'all_all']

iteration_dict["pile-of-law/pile-of-law"]= ['all', 'r_legaladvice', 'courtlistener_docket_entry_documents', 'atticus_contracts', 'courtlistener_opinions', 'federal_register', 'bva_opinions', 'us_bills', 'cc_casebooks', 'tos', 'euro_parl', 'nlrb_decisions', 'scotus_oral_arguments', 'cfr', 'state_codes', 'scotus_filings', 'bar_exam_outlines', 'edgar', 'cfpb_creditcard_contracts', 'constitutions', 'congressional_hearings', 'oig', 'olc_memos', 'uscode', 'founding_docs', 'ftc_advisory_opinions', 'echr', 'eurlex', 'tax_rulings', 'un_debates', 'fre', 'frcp', 'canadian_decisions', 'eoir', 'dol_ecab']

for k, v in iteration_dict.items():
    print('Processing ', k)
    create_overview(k, v)


