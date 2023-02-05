---
annotations_creators:
- other
language_creators:
- found
language:
- bg 
- cs 
- da 
- de 
- el 
- en
- es 
- et 
- fi 
- fr 
- ga
- hr 
- hu 
- it 
- lt 
- lv 
- mt
- nl 
- pl 
- pt 
- ro 
- sk 
- sl 
- sv
license:
- cc-by-4.0
multilinguality:
- multilingual
paperswithcode_id: null
pretty_name: "MultiLegalPileWikipediaFiltered: A filtered version of the MultiLegalPile dataset, together with wikipedia articles."
size_categories:
- 10M<n<100M
source_datasets:
- original
task_categories:
- fill-mask

---

# Dataset Card for MultiLegalPileWikipediaFiltered: A filtered version of the MultiLegalPile dataset, together with wikipedia articles

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Dataset Description](#dataset-description)
    - [Dataset Summary](#dataset-summary)
    - [Supported Tasks and Leaderboards](#supported-tasks-and-leaderboards)
    - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
    - [Data Instances](#data-instances)
    - [Data Fields](#data-fields)
    - [Data Splits](#data-splits)
- [Dataset Creation](#dataset-creation)
    - [Curation Rationale](#curation-rationale)
    - [Source Data](#source-data)
    - [Annotations](#annotations)
    - [Personal and Sensitive Information](#personal-and-sensitive-information)
- [Considerations for Using the Data](#considerations-for-using-the-data)
    - [Social Impact of Dataset](#social-impact-of-dataset)
    - [Discussion of Biases](#discussion-of-biases)
    - [Other Known Limitations](#other-known-limitations)
- [Additional Information](#additional-information)
    - [Dataset Curators](#dataset-curators)
    - [Licensing Information](#licensing-information)
    - [Citation Information](#citation-information)
    - [Contributions](#contributions)

## Dataset Description

- **Homepage:**
- **Repository:** 
- **Paper:** 
- **Leaderboard:**
- **Point of Contact:** [Joel Niklaus](mailto:joel.niklaus.2@bfh.ch)

### Dataset Summary

The Multi_Legal_Pile is a large-scale multilingual legal dataset suited for pretraining language models.
It spans over 24 languages and four legal text types. 

### Supported Tasks and Leaderboards

The dataset supports the tasks of fill-mask.

### Languages

The following languages are supported: 
bg, cs, da, de, el, en, es, et, fi, fr, ga, hr, hu, it, lt, lv, mt, nl, pl, pt, ro, sk, sl, sv

## Dataset Structure

It is structured in the following format: {language}_{text_type}_{shard}.jsonl.xz

text_type is one of the following:

- caselaw
- contracts
- legislation
- other
- wikipedia


Use the dataset like this:
```python
from datasets import load_dataset

config = 'en_contracts' # {language}_{text_type}
dataset = load_dataset('joelito/Multi_Legal_Pile', config, split='train', streaming=True)
```

'config' is a combination of language and text_type, e.g. 'en_contracts' or 'de_caselaw'.
To load all the languages or all the text_types, use 'all' instead of the language or text_type (e.g., '
all_legislation').

### Data Instances

The file format is jsonl.xz and there is a `train` and `validation` split available. 
Since some configurations are very small or non-existent, they might not contain a train split or not be present at all.

The complete dataset consists of five large subsets:
- [Native Multi Legal Pile](https://huggingface.co/datasets/joelito/Multi_Legal_Pile)
- [Eurlex Resources](https://huggingface.co/datasets/joelito/eurlex_resources) 
- [MC4 Legal](https://huggingface.co/datasets/joelito/mc4_legal)
- [Pile of Law](https://huggingface.co/datasets/pile-of-law/pile-of-law)
- [EU Wikipedias](https://huggingface.co/datasets/joelito/EU_Wikipedias)

### Data Fields

[More Information Needed]

### Data Splits

There are two splits: train and validation. The validation split contains 1000 examples and the training split contains the rest of the data.

#### Data Size

```bash
$ xz --list data/*.xz
Strms  Blocks   Compressed Uncompressed  Ratio  Check   Filename
    1       1    167.6 MiB  3’276.3 MiB  0.051  CRC64   data/bg_caselaw_train.0.jsonl.xz
    1       1    502.3 KiB  9’398.0 KiB  0.053  CRC64   data/bg_caselaw_validation.0.jsonl.xz
    1       1     33.4 MiB    700.3 MiB  0.048  CRC64   data/bg_contracts_train.0.jsonl.xz
    1       1  5’989.6 KiB    123.0 MiB  0.048  CRC64   data/bg_contracts_validation.0.jsonl.xz
    1       1    418.5 MiB  8’931.0 MiB  0.047  CRC64   data/bg_legislation_train.0.jsonl.xz
    1       1  5’029.4 KiB    103.1 MiB  0.048  CRC64   data/bg_legislation_validation.0.jsonl.xz
    1       0         32 B          0 B    ---  CRC64   data/bg_other_validation.0.jsonl.xz
    1       1    192.2 MiB  2’488.6 MiB  0.077  CRC64   data/bg_wikipedia_train.0.jsonl.xz
    1       1  1’757.8 KiB     22.9 MiB  0.075  CRC64   data/bg_wikipedia_validation.0.jsonl.xz
    1       1    476.9 MiB  4’126.1 MiB  0.116  CRC64   data/cs_caselaw_train.0.jsonl.xz
    1       1    259.8 MiB  2’556.9 MiB  0.102  CRC64   data/cs_caselaw_train.1.jsonl.xz
    1       1    420.1 KiB  3’370.3 KiB  0.125  CRC64   data/cs_caselaw_validation.0.jsonl.xz
    1       1     24.9 MiB    237.9 MiB  0.105  CRC64   data/cs_contracts_train.0.jsonl.xz
    1       1  4’412.1 KiB     41.7 MiB  0.103  CRC64   data/cs_contracts_validation.0.jsonl.xz
    1       1    361.2 MiB  3’488.9 MiB  0.104  CRC64   data/cs_legislation_train.0.jsonl.xz
    1       1     10.3 MiB     91.6 MiB  0.112  CRC64   data/cs_legislation_validation.0.jsonl.xz
    1       0         32 B          0 B    ---  CRC64   data/cs_other_validation.0.jsonl.xz
    1       1    390.6 MiB  1’939.4 MiB  0.201  CRC64   data/cs_wikipedia_train.0.jsonl.xz
    1       1  2’604.7 KiB     12.2 MiB  0.209  CRC64   data/cs_wikipedia_validation.0.jsonl.xz
    1       1    252.5 MiB  1’529.7 MiB  0.165  CRC64   data/da_caselaw_train.0.jsonl.xz
    1       1    555.9 KiB  3’227.1 KiB  0.172  CRC64   data/da_caselaw_validation.0.jsonl.xz
    1       1     30.1 MiB    233.9 MiB  0.129  CRC64   data/da_contracts_train.0.jsonl.xz
    1       1  2’897.6 KiB     23.6 MiB  0.120  CRC64   data/da_contracts_validation.0.jsonl.xz
    1       1    476.9 MiB  3’325.8 MiB  0.143  CRC64   data/da_legislation_train.0.jsonl.xz
    1       1    237.3 MiB  1’444.5 MiB  0.164  CRC64   data/da_legislation_train.1.jsonl.xz
    1       1  3’232.5 KiB     60.6 MiB  0.052  CRC64   data/da_legislation_validation.0.jsonl.xz
    1       0         32 B          0 B    ---  CRC64   data/da_other_validation.0.jsonl.xz
    1       1    128.8 MiB    512.1 MiB  0.252  CRC64   data/da_wikipedia_train.0.jsonl.xz
    1       1  1’514.1 KiB  5’476.3 KiB  0.276  CRC64   data/da_wikipedia_validation.0.jsonl.xz
    1       1    476.9 MiB  2’803.8 MiB  0.170  CRC64   data/de_caselaw_train.0.jsonl.xz
    1       1    476.9 MiB  2’821.4 MiB  0.169  CRC64   data/de_caselaw_train.1.jsonl.xz
    1       1    476.9 MiB  2’720.2 MiB  0.175  CRC64   data/de_caselaw_train.2.jsonl.xz
    1       1    476.9 MiB  2’704.1 MiB  0.176  CRC64   data/de_caselaw_train.3.jsonl.xz
    1       1    460.5 MiB  2’504.5 MiB  0.184  CRC64   data/de_caselaw_train.4.jsonl.xz
    1       1    594.0 KiB  3’416.4 KiB  0.174  CRC64   data/de_caselaw_validation.0.jsonl.xz
    1       1     32.0 MiB    255.8 MiB  0.125  CRC64   data/de_contracts_train.0.jsonl.xz
    1       1  3’037.7 KiB     24.7 MiB  0.120  CRC64   data/de_contracts_validation.0.jsonl.xz
    1       1    476.9 MiB  3’386.0 MiB  0.141  CRC64   data/de_legislation_train.0.jsonl.xz
    1       1     93.3 MiB    592.3 MiB  0.158  CRC64   data/de_legislation_train.1.jsonl.xz
    1       1  3’265.9 KiB     20.5 MiB  0.156  CRC64   data/de_legislation_validation.0.jsonl.xz
    1       0         32 B          0 B    ---  CRC64   data/de_other_validation.0.jsonl.xz
    1       1    476.9 MiB  1’883.7 MiB  0.253  CRC64   data/de_wikipedia_train.0.jsonl.xz
    1       1    476.9 MiB  1’891.6 MiB  0.252  CRC64   data/de_wikipedia_train.1.jsonl.xz
    1       1    476.9 MiB  1’893.7 MiB  0.252  CRC64   data/de_wikipedia_train.2.jsonl.xz
    1       1    476.9 MiB  1’894.1 MiB  0.252  CRC64   data/de_wikipedia_train.3.jsonl.xz
    1       1    407.9 MiB  1’622.0 MiB  0.251  CRC64   data/de_wikipedia_train.4.jsonl.xz
    1       1  1’172.5 KiB  4’210.2 KiB  0.278  CRC64   data/de_wikipedia_validation.0.jsonl.xz
    1       1    344.7 MiB  6’908.3 MiB  0.050  CRC64   data/el_caselaw_train.0.jsonl.xz
    1       1    870.4 KiB     14.3 MiB  0.060  CRC64   data/el_caselaw_validation.0.jsonl.xz
    1       1     49.7 MiB  1’083.8 MiB  0.046  CRC64   data/el_contracts_train.0.jsonl.xz
    1       1  4’701.3 KiB    101.6 MiB  0.045  CRC64   data/el_contracts_validation.0.jsonl.xz
    1       1    476.9 MiB     10.2 GiB  0.046  CRC64   data/el_legislation_train.0.jsonl.xz
    1       1    203.0 MiB  3’994.0 MiB  0.051  CRC64   data/el_legislation_train.1.jsonl.xz
    1       1  9’744.3 KiB    186.6 MiB  0.051  CRC64   data/el_legislation_validation.0.jsonl.xz
    1       0         32 B          0 B    ---  CRC64   data/el_other_validation.0.jsonl.xz
    1       1    246.4 MiB  3’465.7 MiB  0.071  CRC64   data/el_wikipedia_train.0.jsonl.xz
    1       1  2’591.7 KiB     35.6 MiB  0.071  CRC64   data/el_wikipedia_validation.0.jsonl.xz
    1       1    476.9 MiB  2’188.6 MiB  0.218  CRC64   data/en_caselaw_train.0.jsonl.xz
    1       1    476.9 MiB  2’416.1 MiB  0.197  CRC64   data/en_caselaw_train.10.jsonl.xz
    1       1    477.2 MiB  2’688.1 MiB  0.178  CRC64   data/en_caselaw_train.11.jsonl.xz
    1       1    476.9 MiB  2’865.9 MiB  0.166  CRC64   data/en_caselaw_train.12.jsonl.xz
    1       1    476.9 MiB  2’494.1 MiB  0.191  CRC64   data/en_caselaw_train.13.jsonl.xz
    1       1    476.9 MiB  2’126.6 MiB  0.224  CRC64   data/en_caselaw_train.14.jsonl.xz
    1       1    476.9 MiB  2’440.9 MiB  0.195  CRC64   data/en_caselaw_train.15.jsonl.xz
    1       1    476.9 MiB  3’822.2 MiB  0.125  CRC64   data/en_caselaw_train.16.jsonl.xz
    1       1    476.9 MiB  3’831.4 MiB  0.124  CRC64   data/en_caselaw_train.17.jsonl.xz
    1       1    476.9 MiB  3’812.2 MiB  0.125  CRC64   data/en_caselaw_train.18.jsonl.xz
    1       1    476.9 MiB  2’233.5 MiB  0.214  CRC64   data/en_caselaw_train.19.jsonl.xz
    1       1    476.9 MiB  2’195.9 MiB  0.217  CRC64   data/en_caselaw_train.1.jsonl.xz
    1       1    476.9 MiB  2’185.8 MiB  0.218  CRC64   data/en_caselaw_train.20.jsonl.xz
    1       1    476.9 MiB  2’634.9 MiB  0.181  CRC64   data/en_caselaw_train.21.jsonl.xz
    1       1    476.9 MiB  2’670.8 MiB  0.179  CRC64   data/en_caselaw_train.22.jsonl.xz
    1       1    476.9 MiB  2’762.0 MiB  0.173  CRC64   data/en_caselaw_train.23.jsonl.xz
    1       1    476.9 MiB  2’153.6 MiB  0.221  CRC64   data/en_caselaw_train.24.jsonl.xz
    1       1    476.9 MiB  2’152.0 MiB  0.222  CRC64   data/en_caselaw_train.25.jsonl.xz
    1       1    476.9 MiB  2’205.0 MiB  0.216  CRC64   data/en_caselaw_train.26.jsonl.xz
    1       1    476.9 MiB  2’141.0 MiB  0.223  CRC64   data/en_caselaw_train.27.jsonl.xz
    1       1    476.9 MiB  2’145.1 MiB  0.222  CRC64   data/en_caselaw_train.28.jsonl.xz
    1       1    476.9 MiB  2’137.9 MiB  0.223  CRC64   data/en_caselaw_train.29.jsonl.xz
    1       1    476.9 MiB  2’189.0 MiB  0.218  CRC64   data/en_caselaw_train.2.jsonl.xz
    1       1    476.9 MiB  2’150.9 MiB  0.222  CRC64   data/en_caselaw_train.30.jsonl.xz
    1       1    476.9 MiB  2’142.7 MiB  0.223  CRC64   data/en_caselaw_train.31.jsonl.xz
    1       1    476.9 MiB  2’203.4 MiB  0.216  CRC64   data/en_caselaw_train.32.jsonl.xz
    1       1    476.9 MiB  2’205.4 MiB  0.216  CRC64   data/en_caselaw_train.33.jsonl.xz
    1       1    476.9 MiB  2’206.0 MiB  0.216  CRC64   data/en_caselaw_train.34.jsonl.xz
    1       1    476.9 MiB  2’164.9 MiB  0.220  CRC64   data/en_caselaw_train.35.jsonl.xz
    1       1    476.9 MiB  2’810.3 MiB  0.170  CRC64   data/en_caselaw_train.36.jsonl.xz
    1       1    476.9 MiB  2’854.1 MiB  0.167  CRC64   data/en_caselaw_train.37.jsonl.xz
    1       1    476.9 MiB  3’109.2 MiB  0.153  CRC64   data/en_caselaw_train.38.jsonl.xz
    1       1    476.9 MiB  3’323.6 MiB  0.143  CRC64   data/en_caselaw_train.39.jsonl.xz
    1       1    476.9 MiB  2’155.3 MiB  0.221  CRC64   data/en_caselaw_train.3.jsonl.xz
    1       1    476.9 MiB  2’881.5 MiB  0.165  CRC64   data/en_caselaw_train.40.jsonl.xz
    1       1    476.9 MiB  2’157.1 MiB  0.221  CRC64   data/en_caselaw_train.41.jsonl.xz
    1       1    477.0 MiB  2’530.2 MiB  0.189  CRC64   data/en_caselaw_train.42.jsonl.xz
    1       1    476.8 MiB  2’540.1 MiB  0.188  CRC64   data/en_caselaw_train.43.jsonl.xz
    1       1    476.9 MiB  2’182.2 MiB  0.219  CRC64   data/en_caselaw_train.44.jsonl.xz
    1       1    476.9 MiB  2’163.2 MiB  0.220  CRC64   data/en_caselaw_train.45.jsonl.xz
    1       1    476.9 MiB  2’213.3 MiB  0.215  CRC64   data/en_caselaw_train.46.jsonl.xz
    1       1    476.9 MiB  2’241.5 MiB  0.213  CRC64   data/en_caselaw_train.47.jsonl.xz
    1       1    476.9 MiB  2’203.6 MiB  0.216  CRC64   data/en_caselaw_train.48.jsonl.xz
    1       1    476.9 MiB  2’480.6 MiB  0.192  CRC64   data/en_caselaw_train.49.jsonl.xz
    1       1    476.9 MiB  2’176.7 MiB  0.219  CRC64   data/en_caselaw_train.4.jsonl.xz
    1       1    476.9 MiB  2’214.7 MiB  0.215  CRC64   data/en_caselaw_train.50.jsonl.xz
    1       1    476.9 MiB  2’128.0 MiB  0.224  CRC64   data/en_caselaw_train.51.jsonl.xz
    1       1    476.9 MiB  2’151.0 MiB  0.222  CRC64   data/en_caselaw_train.52.jsonl.xz
    1       1    476.9 MiB  2’173.6 MiB  0.219  CRC64   data/en_caselaw_train.53.jsonl.xz
    1       1    476.9 MiB  2’773.8 MiB  0.172  CRC64   data/en_caselaw_train.54.jsonl.xz
    1       1    476.9 MiB  2’806.2 MiB  0.170  CRC64   data/en_caselaw_train.55.jsonl.xz
    1       1    476.9 MiB  3’920.9 MiB  0.122  CRC64   data/en_caselaw_train.56.jsonl.xz
    1       1    476.9 MiB  2’517.2 MiB  0.189  CRC64   data/en_caselaw_train.57.jsonl.xz
    1       1    477.5 MiB  2’844.0 MiB  0.168  CRC64   data/en_caselaw_train.58.jsonl.xz
    1       1    476.9 MiB  2’810.7 MiB  0.170  CRC64   data/en_caselaw_train.59.jsonl.xz
    1       1    476.9 MiB  2’160.4 MiB  0.221  CRC64   data/en_caselaw_train.5.jsonl.xz
    1       1    476.9 MiB  3’033.0 MiB  0.157  CRC64   data/en_caselaw_train.60.jsonl.xz
    1       1    476.9 MiB  2’255.1 MiB  0.211  CRC64   data/en_caselaw_train.61.jsonl.xz
    1       1    476.9 MiB  2’110.1 MiB  0.226  CRC64   data/en_caselaw_train.62.jsonl.xz
    1       1    476.9 MiB  2’130.3 MiB  0.224  CRC64   data/en_caselaw_train.63.jsonl.xz
    1       1    476.9 MiB  2’133.2 MiB  0.224  CRC64   data/en_caselaw_train.64.jsonl.xz
    1       1     44.8 MiB    199.6 MiB  0.225  CRC64   data/en_caselaw_train.65.jsonl.xz
    1       1    476.9 MiB  2’153.3 MiB  0.221  CRC64   data/en_caselaw_train.6.jsonl.xz
    1       1    476.9 MiB  2’130.8 MiB  0.224  CRC64   data/en_caselaw_train.7.jsonl.xz
    1       1    476.9 MiB  2’152.2 MiB  0.222  CRC64   data/en_caselaw_train.8.jsonl.xz
    1       1    476.9 MiB  2’173.3 MiB  0.219  CRC64   data/en_caselaw_train.9.jsonl.xz
    1       1  2’977.4 KiB     12.9 MiB  0.226  CRC64   data/en_caselaw_validation.0.jsonl.xz
    1       1    476.9 MiB  3’016.6 MiB  0.158  CRC64   data/en_contracts_train.0.jsonl.xz
    1       1    476.9 MiB  3’015.3 MiB  0.158  CRC64   data/en_contracts_train.10.jsonl.xz
    1       1    476.9 MiB  3’012.5 MiB  0.158  CRC64   data/en_contracts_train.11.jsonl.xz
    1       1    477.0 MiB  3’002.5 MiB  0.159  CRC64   data/en_contracts_train.12.jsonl.xz
    1       1    476.9 MiB  2’962.4 MiB  0.161  CRC64   data/en_contracts_train.13.jsonl.xz
    1       1    476.9 MiB  3’019.4 MiB  0.158  CRC64   data/en_contracts_train.14.jsonl.xz
    1       1    124.1 MiB    781.2 MiB  0.159  CRC64   data/en_contracts_train.15.jsonl.xz
    1       1    476.9 MiB  2’994.0 MiB  0.159  CRC64   data/en_contracts_train.1.jsonl.xz
    1       1    476.8 MiB  3’084.9 MiB  0.155  CRC64   data/en_contracts_train.2.jsonl.xz
    1       1    476.9 MiB  3’123.4 MiB  0.153  CRC64   data/en_contracts_train.3.jsonl.xz
    1       1    476.9 MiB  3’120.7 MiB  0.153  CRC64   data/en_contracts_train.4.jsonl.xz
    1       1    477.0 MiB  3’094.2 MiB  0.154  CRC64   data/en_contracts_train.5.jsonl.xz
    1       1    476.9 MiB  3’010.9 MiB  0.158  CRC64   data/en_contracts_train.6.jsonl.xz
    1       1    476.9 MiB  3’015.0 MiB  0.158  CRC64   data/en_contracts_train.7.jsonl.xz
    1       1    476.9 MiB  2’995.7 MiB  0.159  CRC64   data/en_contracts_train.8.jsonl.xz
    1       1    476.9 MiB  3’017.9 MiB  0.158  CRC64   data/en_contracts_train.9.jsonl.xz
    1       1  9’980.4 KiB     63.7 MiB  0.153  CRC64   data/en_contracts_validation.0.jsonl.xz
    1       1    476.9 MiB  3’040.8 MiB  0.157  CRC64   data/en_legislation_train.0.jsonl.xz
    1       1    476.9 MiB  3’047.3 MiB  0.156  CRC64   data/en_legislation_train.1.jsonl.xz
    1       1    476.9 MiB  3’351.5 MiB  0.142  CRC64   data/en_legislation_train.2.jsonl.xz
    1       1    478.7 MiB  3’408.4 MiB  0.140  CRC64   data/en_legislation_train.3.jsonl.xz
    1       1    372.5 MiB  2’620.0 MiB  0.142  CRC64   data/en_legislation_train.4.jsonl.xz
    1       1  2’733.5 KiB     13.8 MiB  0.193  CRC64   data/en_legislation_validation.0.jsonl.xz
    1       1    476.9 MiB  4’782.4 MiB  0.100  CRC64   data/en_other_train.0.jsonl.xz
    1       1    476.9 MiB  4’347.1 MiB  0.110  CRC64   data/en_other_train.10.jsonl.xz
    1       1    477.1 MiB  3’044.6 MiB  0.157  CRC64   data/en_other_train.11.jsonl.xz
    1       1    477.1 MiB  2’147.8 MiB  0.222  CRC64   data/en_other_train.12.jsonl.xz
    1       1    477.0 MiB  2’182.8 MiB  0.219  CRC64   data/en_other_train.13.jsonl.xz
    1       1     33.3 MiB    151.7 MiB  0.219  CRC64   data/en_other_train.14.jsonl.xz
    1       1    476.9 MiB  4’883.8 MiB  0.098  CRC64   data/en_other_train.1.jsonl.xz
    1       1    476.9 MiB  4’646.7 MiB  0.103  CRC64   data/en_other_train.2.jsonl.xz
    1       1    476.9 MiB  4’542.8 MiB  0.105  CRC64   data/en_other_train.3.jsonl.xz
    1       1    476.9 MiB  4’574.8 MiB  0.104  CRC64   data/en_other_train.4.jsonl.xz
    1       1    476.9 MiB  4’622.5 MiB  0.103  CRC64   data/en_other_train.5.jsonl.xz
    1       1    476.9 MiB  4’520.7 MiB  0.105  CRC64   data/en_other_train.6.jsonl.xz
    1       1    476.9 MiB  2’942.4 MiB  0.162  CRC64   data/en_other_train.7.jsonl.xz
    1       1    476.9 MiB  2’544.0 MiB  0.187  CRC64   data/en_other_train.8.jsonl.xz
    1       1    476.9 MiB  4’515.4 MiB  0.106  CRC64   data/en_other_train.9.jsonl.xz
    1       1  2’165.8 KiB     19.6 MiB  0.108  CRC64   data/en_other_validation.0.jsonl.xz
    1       1    476.9 MiB  1’803.2 MiB  0.264  CRC64   data/en_wikipedia_train.0.jsonl.xz
    1       1    441.1 MiB  1’670.5 MiB  0.264  CRC64   data/en_wikipedia_train.10.jsonl.xz
    1       1    476.9 MiB  1’803.6 MiB  0.264  CRC64   data/en_wikipedia_train.1.jsonl.xz
    1       1    476.9 MiB  1’802.5 MiB  0.265  CRC64   data/en_wikipedia_train.2.jsonl.xz
    1       1    476.9 MiB  1’805.0 MiB  0.264  CRC64   data/en_wikipedia_train.3.jsonl.xz
    1       1    476.9 MiB  1’804.3 MiB  0.264  CRC64   data/en_wikipedia_train.4.jsonl.xz
    1       1    476.9 MiB  1’804.0 MiB  0.264  CRC64   data/en_wikipedia_train.5.jsonl.xz
    1       1    476.9 MiB  1’804.1 MiB  0.264  CRC64   data/en_wikipedia_train.6.jsonl.xz
    1       1    476.9 MiB  1’803.6 MiB  0.264  CRC64   data/en_wikipedia_train.7.jsonl.xz
    1       1    476.9 MiB  1’805.2 MiB  0.264  CRC64   data/en_wikipedia_train.8.jsonl.xz
    1       1    476.9 MiB  1’804.3 MiB  0.264  CRC64   data/en_wikipedia_train.9.jsonl.xz
    1       1  1’004.9 KiB  3’492.7 KiB  0.288  CRC64   data/en_wikipedia_validation.0.jsonl.xz
    1       1    216.4 MiB  1’458.0 MiB  0.148  CRC64   data/es_caselaw_train.0.jsonl.xz
    1       1    586.4 KiB  3’537.8 KiB  0.166  CRC64   data/es_caselaw_validation.0.jsonl.xz
    1       1     29.0 MiB    244.0 MiB  0.119  CRC64   data/es_contracts_train.0.jsonl.xz
    1       1  3’826.2 KiB     31.2 MiB  0.120  CRC64   data/es_contracts_validation.0.jsonl.xz
    1       1    401.8 MiB  3’054.9 MiB  0.132  CRC64   data/es_legislation_train.0.jsonl.xz
    1       1  8’217.6 KiB     56.6 MiB  0.142  CRC64   data/es_legislation_validation.0.jsonl.xz
    1       0         32 B          0 B    ---  CRC64   data/es_other_validation.0.jsonl.xz
    1       1    476.9 MiB  2’017.9 MiB  0.236  CRC64   data/es_wikipedia_train.0.jsonl.xz
    1       1    476.9 MiB  2’025.0 MiB  0.235  CRC64   data/es_wikipedia_train.1.jsonl.xz
    1       1    308.8 MiB  1’305.6 MiB  0.237  CRC64   data/es_wikipedia_train.2.jsonl.xz
    1       1  1’339.7 KiB  5’265.5 KiB  0.254  CRC64   data/es_wikipedia_validation.0.jsonl.xz
    1       1    132.5 MiB    831.3 MiB  0.159  CRC64   data/et_caselaw_train.0.jsonl.xz
    1       1    387.2 KiB  2’310.9 KiB  0.168  CRC64   data/et_caselaw_validation.0.jsonl.xz
    1       1     22.9 MiB    179.6 MiB  0.128  CRC64   data/et_contracts_train.0.jsonl.xz
    1       1  3’164.3 KiB     26.8 MiB  0.115  CRC64   data/et_contracts_validation.0.jsonl.xz
    1       1    255.2 MiB  1’908.2 MiB  0.134  CRC64   data/et_legislation_train.0.jsonl.xz
    1       1  9’239.2 KiB     64.7 MiB  0.140  CRC64   data/et_legislation_validation.0.jsonl.xz
    1       0         32 B          0 B    ---  CRC64   data/et_other_validation.0.jsonl.xz
    1       1    100.5 MiB    408.8 MiB  0.246  CRC64   data/et_wikipedia_train.0.jsonl.xz
    1       1  1’352.2 KiB  4’921.0 KiB  0.275  CRC64   data/et_wikipedia_validation.0.jsonl.xz
    1       1    194.5 MiB  1’359.0 MiB  0.143  CRC64   data/fi_caselaw_train.0.jsonl.xz
    1       1    604.1 KiB  3’656.1 KiB  0.165  CRC64   data/fi_caselaw_validation.0.jsonl.xz
    1       1     26.0 MiB    219.8 MiB  0.118  CRC64   data/fi_contracts_train.0.jsonl.xz
    1       1  2’971.2 KiB     27.4 MiB  0.106  CRC64   data/fi_contracts_validation.0.jsonl.xz
    1       1    334.7 MiB  2’599.3 MiB  0.129  CRC64   data/fi_legislation_train.0.jsonl.xz
    1       1  7’476.3 KiB     53.9 MiB  0.136  CRC64   data/fi_legislation_validation.0.jsonl.xz
    1       0         32 B          0 B    ---  CRC64   data/fi_other_validation.0.jsonl.xz
    1       1    255.6 MiB  1’118.0 MiB  0.229  CRC64   data/fi_wikipedia_train.0.jsonl.xz
    1       1  2’464.2 KiB      9.9 MiB  0.242  CRC64   data/fi_wikipedia_validation.0.jsonl.xz
    1       1    476.9 MiB  3’128.1 MiB  0.152  CRC64   data/fr_caselaw_train.0.jsonl.xz
    1       1    476.9 MiB  3’104.4 MiB  0.154  CRC64   data/fr_caselaw_train.1.jsonl.xz
    1       1    350.2 MiB  2’194.9 MiB  0.160  CRC64   data/fr_caselaw_train.2.jsonl.xz
    1       1    603.0 KiB  3’778.7 KiB  0.160  CRC64   data/fr_caselaw_validation.0.jsonl.xz
    1       1     31.9 MiB    278.3 MiB  0.115  CRC64   data/fr_contracts_train.0.jsonl.xz
    1       1  3’034.4 KiB     26.6 MiB  0.111  CRC64   data/fr_contracts_validation.0.jsonl.xz
    1       1    477.0 MiB  3’721.8 MiB  0.128  CRC64   data/fr_legislation_train.0.jsonl.xz
    1       1     89.3 MiB    670.9 MiB  0.133  CRC64   data/fr_legislation_train.1.jsonl.xz
    1       1  3’185.5 KiB     22.6 MiB  0.138  CRC64   data/fr_legislation_validation.0.jsonl.xz
    1       0         32 B          0 B    ---  CRC64   data/fr_other_validation.0.jsonl.xz
    1       1    476.9 MiB  2’150.5 MiB  0.222  CRC64   data/fr_wikipedia_train.0.jsonl.xz
    1       1    476.9 MiB  2’151.4 MiB  0.222  CRC64   data/fr_wikipedia_train.1.jsonl.xz
    1       1    476.9 MiB  2’151.2 MiB  0.222  CRC64   data/fr_wikipedia_train.2.jsonl.xz
    1       1    384.8 MiB  1’736.1 MiB  0.222  CRC64   data/fr_wikipedia_train.3.jsonl.xz
    1       1    937.8 KiB  3’777.6 KiB  0.248  CRC64   data/fr_wikipedia_validation.0.jsonl.xz
    1       1    721.9 KiB  5’663.9 KiB  0.127  CRC64   data/ga_caselaw_validation.0.jsonl.xz
    1       1  1’246.1 KiB     15.6 MiB  0.078  CRC64   data/ga_contracts_validation.0.jsonl.xz
    1       1     41.2 MiB    419.0 MiB  0.098  CRC64   data/ga_legislation_train.0.jsonl.xz
    1       1     14.9 MiB    123.2 MiB  0.121  CRC64   data/ga_legislation_validation.0.jsonl.xz
    1       0         32 B          0 B    ---  CRC64   data/ga_other_validation.0.jsonl.xz
    1       1     11.0 MiB     52.9 MiB  0.207  CRC64   data/ga_wikipedia_train.0.jsonl.xz
    1       1    782.4 KiB  3’438.9 KiB  0.228  CRC64   data/ga_wikipedia_validation.0.jsonl.xz
    1       1     72.7 MiB    460.3 MiB  0.158  CRC64   data/hr_caselaw_train.0.jsonl.xz
    1       1    359.9 KiB  2’214.8 KiB  0.162  CRC64   data/hr_caselaw_validation.0.jsonl.xz
    1       1     21.2 MiB    158.3 MiB  0.134  CRC64   data/hr_contracts_train.0.jsonl.xz
    1       1  3’785.9 KiB     26.6 MiB  0.139  CRC64   data/hr_contracts_validation.0.jsonl.xz
    1       1    160.6 MiB  1’258.7 MiB  0.128  CRC64   data/hr_legislation_train.0.jsonl.xz
    1       1     11.2 MiB     86.1 MiB  0.130  CRC64   data/hr_legislation_validation.0.jsonl.xz
    1       0         32 B          0 B    ---  CRC64   data/hr_other_validation.0.jsonl.xz
    1       1    110.3 MiB    425.5 MiB  0.259  CRC64   data/hr_wikipedia_train.0.jsonl.xz
    1       1  1’743.8 KiB  6’170.1 KiB  0.283  CRC64   data/hr_wikipedia_validation.0.jsonl.xz
    1       1    150.6 MiB  1’320.5 MiB  0.114  CRC64   data/hu_caselaw_train.0.jsonl.xz
    1       1    423.8 KiB  3’496.6 KiB  0.121  CRC64   data/hu_caselaw_validation.0.jsonl.xz
    1       1     26.9 MiB    266.0 MiB  0.101  CRC64   data/hu_contracts_train.0.jsonl.xz
    1       1  3’532.6 KiB     36.1 MiB  0.096  CRC64   data/hu_contracts_validation.0.jsonl.xz
    1       1    337.6 MiB  3’129.4 MiB  0.108  CRC64   data/hu_legislation_train.0.jsonl.xz
    1       1  3’913.7 KiB     94.8 MiB  0.040  CRC64   data/hu_legislation_validation.0.jsonl.xz
    1       0         32 B          0 B    ---  CRC64   data/hu_other_validation.0.jsonl.xz
    1       1    364.2 MiB  1’835.0 MiB  0.198  CRC64   data/hu_wikipedia_train.0.jsonl.xz
    1       1  1’719.5 KiB  8’000.8 KiB  0.215  CRC64   data/hu_wikipedia_validation.0.jsonl.xz
    1       1    459.8 MiB  2’742.8 MiB  0.168  CRC64   data/it_caselaw_train.0.jsonl.xz
    1       1    577.8 KiB  3’194.2 KiB  0.181  CRC64   data/it_caselaw_validation.0.jsonl.xz
    1       1     31.2 MiB    240.4 MiB  0.130  CRC64   data/it_contracts_train.0.jsonl.xz
    1       1  3’068.9 KiB     24.0 MiB  0.125  CRC64   data/it_contracts_validation.0.jsonl.xz
    1       1    476.9 MiB  3’362.3 MiB  0.142  CRC64   data/it_legislation_train.0.jsonl.xz
    1       1     38.9 MiB    238.7 MiB  0.163  CRC64   data/it_legislation_train.1.jsonl.xz
    1       1  3’211.3 KiB     25.3 MiB  0.124  CRC64   data/it_legislation_validation.0.jsonl.xz
    1       0         32 B          0 B    ---  CRC64   data/it_other_validation.0.jsonl.xz
    1       1    476.9 MiB  1’864.5 MiB  0.256  CRC64   data/it_wikipedia_train.0.jsonl.xz
    1       1    476.9 MiB  1’864.8 MiB  0.256  CRC64   data/it_wikipedia_train.1.jsonl.xz
    1       1    184.6 MiB    726.2 MiB  0.254  CRC64   data/it_wikipedia_train.2.jsonl.xz
    1       1  1’334.0 KiB  4’843.5 KiB  0.275  CRC64   data/it_wikipedia_validation.0.jsonl.xz
    1       1    136.6 MiB    975.7 MiB  0.140  CRC64   data/lt_caselaw_train.0.jsonl.xz
    1       1    397.0 KiB  2’660.9 KiB  0.149  CRC64   data/lt_caselaw_validation.0.jsonl.xz
    1       1     24.9 MiB    211.8 MiB  0.118  CRC64   data/lt_contracts_train.0.jsonl.xz
    1       1  3’275.5 KiB     26.1 MiB  0.123  CRC64   data/lt_contracts_validation.0.jsonl.xz
    1       1    274.0 MiB  2’174.1 MiB  0.126  CRC64   data/lt_legislation_train.0.jsonl.xz
    1       1  9’780.7 KiB     73.4 MiB  0.130  CRC64   data/lt_legislation_validation.0.jsonl.xz
    1       0         32 B          0 B    ---  CRC64   data/lt_other_validation.0.jsonl.xz
    1       1     72.6 MiB    349.5 MiB  0.208  CRC64   data/lt_wikipedia_train.0.jsonl.xz
    1       1  1’251.2 KiB  5’369.5 KiB  0.233  CRC64   data/lt_wikipedia_validation.0.jsonl.xz
    1       1    141.0 MiB  1’106.7 MiB  0.127  CRC64   data/lv_caselaw_train.0.jsonl.xz
    1       1    410.3 KiB  3’004.0 KiB  0.137  CRC64   data/lv_caselaw_validation.0.jsonl.xz
    1       1     24.9 MiB    224.5 MiB  0.111  CRC64   data/lv_contracts_train.0.jsonl.xz
    1       1  3’629.0 KiB     33.6 MiB  0.106  CRC64   data/lv_contracts_validation.0.jsonl.xz
    1       1    271.5 MiB  2’377.4 MiB  0.114  CRC64   data/lv_legislation_train.0.jsonl.xz
    1       1     10.5 MiB     87.5 MiB  0.120  CRC64   data/lv_legislation_validation.0.jsonl.xz
    1       0         32 B          0 B    ---  CRC64   data/lv_other_validation.0.jsonl.xz
    1       1     47.5 MiB    254.7 MiB  0.186  CRC64   data/lv_wikipedia_train.0.jsonl.xz
    1       1    984.1 KiB  4’559.4 KiB  0.216  CRC64   data/lv_wikipedia_validation.0.jsonl.xz
    1       1    132.2 MiB    956.6 MiB  0.138  CRC64   data/mt_caselaw_train.0.jsonl.xz
    1       1    396.1 KiB  2’680.0 KiB  0.148  CRC64   data/mt_caselaw_validation.0.jsonl.xz
    1       1     25.6 MiB    201.0 MiB  0.127  CRC64   data/mt_contracts_train.0.jsonl.xz
    1       1  4’178.4 KiB     34.0 MiB  0.120  CRC64   data/mt_contracts_validation.0.jsonl.xz
    1       1    270.7 MiB  2’121.7 MiB  0.128  CRC64   data/mt_legislation_train.0.jsonl.xz
    1       1     11.4 MiB     84.2 MiB  0.135  CRC64   data/mt_legislation_validation.0.jsonl.xz
    1       0         32 B          0 B    ---  CRC64   data/mt_other_validation.0.jsonl.xz
    1       1  4’608.3 KiB     19.5 MiB  0.231  CRC64   data/mt_wikipedia_train.0.jsonl.xz
    1       1  1’405.0 KiB  5’754.4 KiB  0.244  CRC64   data/mt_wikipedia_validation.0.jsonl.xz
    1       1    223.1 MiB  1’338.9 MiB  0.167  CRC64   data/nl_caselaw_train.0.jsonl.xz
    1       1    566.0 KiB  3’152.2 KiB  0.180  CRC64   data/nl_caselaw_validation.0.jsonl.xz
    1       1     31.6 MiB    242.3 MiB  0.130  CRC64   data/nl_contracts_train.0.jsonl.xz
    1       1  2’663.9 KiB     22.4 MiB  0.116  CRC64   data/nl_contracts_validation.0.jsonl.xz
    1       1    476.9 MiB  3’311.9 MiB  0.144  CRC64   data/nl_legislation_train.0.jsonl.xz
    1       1     41.1 MiB    268.7 MiB  0.153  CRC64   data/nl_legislation_train.1.jsonl.xz
    1       1  3’678.8 KiB     72.9 MiB  0.049  CRC64   data/nl_legislation_validation.0.jsonl.xz
    1       0         32 B          0 B    ---  CRC64   data/nl_other_validation.0.jsonl.xz
    1       1    476.9 MiB  1’856.9 MiB  0.257  CRC64   data/nl_wikipedia_train.0.jsonl.xz
    1       1     59.9 MiB    236.4 MiB  0.253  CRC64   data/nl_wikipedia_train.1.jsonl.xz
    1       1    979.4 KiB  3’414.8 KiB  0.287  CRC64   data/nl_wikipedia_validation.0.jsonl.xz
    1       1    147.9 MiB  1’034.1 MiB  0.143  CRC64   data/pl_caselaw_train.0.jsonl.xz
    1       1    416.2 KiB  2’737.2 KiB  0.152  CRC64   data/pl_caselaw_validation.0.jsonl.xz
    1       1     24.8 MiB    208.9 MiB  0.119  CRC64   data/pl_contracts_train.0.jsonl.xz
    1       1  4’241.9 KiB     34.6 MiB  0.120  CRC64   data/pl_contracts_validation.0.jsonl.xz
    1       1    325.0 MiB  2’646.2 MiB  0.123  CRC64   data/pl_legislation_train.0.jsonl.xz
    1       1  3’593.0 KiB     29.0 MiB  0.121  CRC64   data/pl_legislation_validation.0.jsonl.xz
    1       0         32 B          0 B    ---  CRC64   data/pl_other_validation.0.jsonl.xz
    1       1    476.9 MiB  2’144.7 MiB  0.222  CRC64   data/pl_wikipedia_train.0.jsonl.xz
    1       1    189.5 MiB    864.0 MiB  0.219  CRC64   data/pl_wikipedia_train.1.jsonl.xz
    1       1  1’233.2 KiB  4’965.9 KiB  0.248  CRC64   data/pl_wikipedia_validation.0.jsonl.xz
    1       1    476.9 MiB  3’494.2 MiB  0.136  CRC64   data/pt_caselaw_train.0.jsonl.xz
    1       1    476.9 MiB  3’392.1 MiB  0.141  CRC64   data/pt_caselaw_train.10.jsonl.xz
    1       1    476.9 MiB  3’505.3 MiB  0.136  CRC64   data/pt_caselaw_train.11.jsonl.xz
    1       1    476.9 MiB  3’524.1 MiB  0.135  CRC64   data/pt_caselaw_train.12.jsonl.xz
    1       1    476.9 MiB  3’458.4 MiB  0.138  CRC64   data/pt_caselaw_train.13.jsonl.xz
    1       1    476.9 MiB  3’602.9 MiB  0.132  CRC64   data/pt_caselaw_train.14.jsonl.xz
    1       1    476.9 MiB  4’923.4 MiB  0.097  CRC64   data/pt_caselaw_train.15.jsonl.xz
    1       1    476.9 MiB  6’648.8 MiB  0.072  CRC64   data/pt_caselaw_train.16.jsonl.xz
    1       1    476.9 MiB  7’461.0 MiB  0.064  CRC64   data/pt_caselaw_train.17.jsonl.xz
    1       1    476.9 MiB  6’866.4 MiB  0.069  CRC64   data/pt_caselaw_train.18.jsonl.xz
    1       1    476.9 MiB  3’455.7 MiB  0.138  CRC64   data/pt_caselaw_train.19.jsonl.xz
    1       1    476.9 MiB  3’513.7 MiB  0.136  CRC64   data/pt_caselaw_train.1.jsonl.xz
    1       1    476.9 MiB  3’477.3 MiB  0.137  CRC64   data/pt_caselaw_train.20.jsonl.xz
    1       1    476.9 MiB  3’492.8 MiB  0.137  CRC64   data/pt_caselaw_train.21.jsonl.xz
    1       1    476.9 MiB  3’528.6 MiB  0.135  CRC64   data/pt_caselaw_train.22.jsonl.xz
    1       1     94.1 MiB    694.3 MiB  0.135  CRC64   data/pt_caselaw_train.23.jsonl.xz
    1       1    476.9 MiB  3’436.5 MiB  0.139  CRC64   data/pt_caselaw_train.2.jsonl.xz
    1       1    476.9 MiB  3’527.9 MiB  0.135  CRC64   data/pt_caselaw_train.3.jsonl.xz
    1       1    476.9 MiB  3’492.2 MiB  0.137  CRC64   data/pt_caselaw_train.4.jsonl.xz
    1       1    476.9 MiB  3’554.8 MiB  0.134  CRC64   data/pt_caselaw_train.5.jsonl.xz
    1       1    476.9 MiB  3’494.7 MiB  0.136  CRC64   data/pt_caselaw_train.6.jsonl.xz
    1       1    476.9 MiB  3’439.1 MiB  0.139  CRC64   data/pt_caselaw_train.7.jsonl.xz
    1       1    476.9 MiB  3’625.6 MiB  0.132  CRC64   data/pt_caselaw_train.8.jsonl.xz
    1       1    476.9 MiB  3’726.4 MiB  0.128  CRC64   data/pt_caselaw_train.9.jsonl.xz
    1       1    798.9 KiB  4’820.6 KiB  0.166  CRC64   data/pt_caselaw_validation.0.jsonl.xz
    1       1     28.4 MiB    243.2 MiB  0.117  CRC64   data/pt_contracts_train.0.jsonl.xz
    1       1  3’899.7 KiB     32.6 MiB  0.117  CRC64   data/pt_contracts_validation.0.jsonl.xz
    1       1    406.2 MiB  3’217.5 MiB  0.126  CRC64   data/pt_legislation_train.0.jsonl.xz
    1       1  8’350.4 KiB     58.4 MiB  0.140  CRC64   data/pt_legislation_validation.0.jsonl.xz
    1       0         32 B          0 B    ---  CRC64   data/pt_other_validation.0.jsonl.xz
    1       1    476.9 MiB  2’050.4 MiB  0.233  CRC64   data/pt_wikipedia_train.0.jsonl.xz
    1       1    140.6 MiB    617.4 MiB  0.228  CRC64   data/pt_wikipedia_train.1.jsonl.xz
    1       1  1’480.0 KiB  6’344.8 KiB  0.233  CRC64   data/pt_wikipedia_validation.0.jsonl.xz
    1       1    124.9 MiB    956.9 MiB  0.131  CRC64   data/ro_caselaw_train.0.jsonl.xz
    1       1    400.4 KiB  2’785.0 KiB  0.144  CRC64   data/ro_caselaw_validation.0.jsonl.xz
    1       1     24.6 MiB    210.5 MiB  0.117  CRC64   data/ro_contracts_train.0.jsonl.xz
    1       1  3’886.3 KiB     34.3 MiB  0.111  CRC64   data/ro_contracts_validation.0.jsonl.xz
    1       1    476.9 MiB  4’496.4 MiB  0.106  CRC64   data/ro_legislation_train.0.jsonl.xz
    1       1     97.6 MiB  1’053.6 MiB  0.093  CRC64   data/ro_legislation_train.1.jsonl.xz
    1       1  3’691.3 KiB     33.4 MiB  0.108  CRC64   data/ro_legislation_validation.0.jsonl.xz
    1       0         32 B          0 B    ---  CRC64   data/ro_other_validation.0.jsonl.xz
    1       1    179.7 MiB    833.0 MiB  0.216  CRC64   data/ro_wikipedia_train.0.jsonl.xz
    1       1  2’089.4 KiB  9’053.5 KiB  0.231  CRC64   data/ro_wikipedia_validation.0.jsonl.xz
    1       1    143.6 MiB  1’094.2 MiB  0.131  CRC64   data/sk_caselaw_train.0.jsonl.xz
    1       1    415.8 KiB  3’012.4 KiB  0.138  CRC64   data/sk_caselaw_validation.0.jsonl.xz
    1       1     25.9 MiB    226.7 MiB  0.114  CRC64   data/sk_contracts_train.0.jsonl.xz
    1       1  3’933.6 KiB     35.2 MiB  0.109  CRC64   data/sk_contracts_validation.0.jsonl.xz
    1       1    322.4 MiB  2’745.5 MiB  0.117  CRC64   data/sk_legislation_train.0.jsonl.xz
    1       1  3’735.8 KiB     31.7 MiB  0.115  CRC64   data/sk_legislation_validation.0.jsonl.xz
    1       0         32 B          0 B    ---  CRC64   data/sk_other_validation.0.jsonl.xz
    1       1     91.2 MiB    435.3 MiB  0.210  CRC64   data/sk_wikipedia_train.0.jsonl.xz
    1       1  1’724.4 KiB  7’568.3 KiB  0.228  CRC64   data/sk_wikipedia_validation.0.jsonl.xz
    1       1    131.9 MiB    815.8 MiB  0.162  CRC64   data/sl_caselaw_train.0.jsonl.xz
    1       1    392.8 KiB  2’328.2 KiB  0.169  CRC64   data/sl_caselaw_validation.0.jsonl.xz
    1       1     22.9 MiB    172.4 MiB  0.133  CRC64   data/sl_contracts_train.0.jsonl.xz
    1       1  3’493.7 KiB     27.2 MiB  0.125  CRC64   data/sl_contracts_validation.0.jsonl.xz
    1       1    388.1 MiB  2’732.3 MiB  0.142  CRC64   data/sl_legislation_train.0.jsonl.xz
    1       1  3’429.8 KiB     24.3 MiB  0.138  CRC64   data/sl_legislation_validation.0.jsonl.xz
    1       0         32 B          0 B    ---  CRC64   data/sl_other_validation.0.jsonl.xz
    1       1    104.6 MiB    425.6 MiB  0.246  CRC64   data/sl_wikipedia_train.0.jsonl.xz
    1       1  1’392.8 KiB  5’004.9 KiB  0.278  CRC64   data/sl_wikipedia_validation.0.jsonl.xz
    1       1    189.5 MiB  1’325.4 MiB  0.143  CRC64   data/sv_caselaw_train.0.jsonl.xz
    1       1    581.2 KiB  3’566.7 KiB  0.163  CRC64   data/sv_caselaw_validation.0.jsonl.xz
    1       1     25.3 MiB    211.7 MiB  0.119  CRC64   data/sv_contracts_train.0.jsonl.xz
    1       1  2’890.6 KiB     26.0 MiB  0.108  CRC64   data/sv_contracts_validation.0.jsonl.xz
    1       1    324.5 MiB  2’570.4 MiB  0.126  CRC64   data/sv_legislation_train.0.jsonl.xz
    1       1  6’984.8 KiB     50.1 MiB  0.136  CRC64   data/sv_legislation_validation.0.jsonl.xz
    1       0         32 B          0 B    ---  CRC64   data/sv_other_validation.0.jsonl.xz
    1       1    333.4 MiB  1’668.1 MiB  0.200  CRC64   data/sv_wikipedia_train.0.jsonl.xz
    1       1  1’088.6 KiB  4’372.9 KiB  0.249  CRC64   data/sv_wikipedia_validation.0.jsonl.xz
-------------------------------------------------------------------------------
  374     351     90.1 GiB    579.9 GiB  0.155  CRC64   374 files
```

## Dataset Creation

This dataset has been created by combining the following datasets:
Native Multi Legal Pile, Eurlex Resources, MC4 Legal, Pile of Law, EU Wikipedias.
It has been filtered to remove short documents (less than 64 whitespace-separated tokens) and 
documents with more than 30% punctuation or numbers (see prepare_legal_data.py for more details).

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]


### Annotations

#### Annotation process

[More Information Needed]

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

[More Information Needed]

### Licensing Information

[More Information Needed]

### Citation Information

```
TODO add citation
```

### Contributions

Thanks to [@JoelNiklaus](https://github.com/joelniklaus) for adding this dataset.
