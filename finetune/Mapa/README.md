---
annotations_creators:
- other
language_creators:
- found
language:
- multilingual
language_bcp47:
- bg, cs, da, de, el, en, es, et, fi, fr, ga, hu, it, lt, lv, mt, nl, pt, ro, sk, sv
license:
- cc-by-4.0
multilinguality:
- multilingual
paperswithcode_id: null
pretty_name: Spanish Datasets for Sensitive Entity Detection in the Legal Domain
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- token-classification
task_ids:
- named-entity-recognition
- named entity recognition and classification (NERC)

---

# Dataset Card for Multilingual European Datasets for Sensitive Entity Detection in the Legal Domain

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
- **
  Repository:** [Spanish](https://elrc-share.eu/repository/browse/mapa-anonymization-package-spanish/b550e1a88a8311ec9c1a00155d026706687917f92f64482587c6382175dffd76/), [Most](https://elrc-share.eu/repository/search/?q=mfsp:3222a6048a8811ec9c1a00155d0267067eb521077db54d6684fb14ce8491a391), [German, Portuguese, Slovak, Slovenian, Swedish](https://elrc-share.eu/repository/search/?q=mfsp:833df1248a8811ec9c1a00155d0267067685dcdb77064822b51cc16ab7b81a36)
- **Paper:** de Gibert Bonet, O., García Pablos, A., Cuadros, M., & Melero, M. (2022). Spanish Datasets for Sensitive
  Entity Detection in the Legal Domain. Proceedings of the Language Resources and Evaluation Conference, June,
  3751–3760. http://www.lrec-conf.org/proceedings/lrec2022/pdf/2022.lrec-1.400.pdf
- **Leaderboard:**
- **Point of Contact:** [Joel Niklaus](joel.niklaus.2@bfh.ch)

### Dataset Summary

The dataset consists of 12 documents (9 for Spanish due to parsing errors) taken from EUR-Lex, a multilingual corpus of court
decisions and legal dispositions in the 24 official languages of the European Union. The documents have been annotated
for named entities following the guidelines of the [MAPA project]( https://mapa-project.eu/) which foresees two
annotation level, a general and a more fine-grained one. The annotated corpus can be used for named entity recognition/classification.

### Supported Tasks and Leaderboards

The dataset supports the task of Named Entity Recognition and Classification (NERC).

### Languages

The following languages are supported: bg, cs, da, de, el, en, es, et, fi, fr, ga, hu, it, lt, lv, mt, nl, pt, ro, sk, sv

## Dataset Structure

### Data Instances

The file format is jsonl and three data splits are present (train, validation and test). Named Entity annotations are
non-overlapping.

### Data Fields

For the annotation the documents have been split into sentences. The annotations has been done on the token level. 
The files contain the following data fields

- `language`: language of the sentence
- `type`:  The document type of the sentence. Currently, only EUR-LEX is supported.
- `file_name`: The document file name the sentence belongs to.
- `sentence_number`: The number of the sentence inside its document.
- `tokens`: The list of tokens in the sentence.
- `coarse_grained`: The coarse-grained annotations for each token
- `fine_grained`: The fine-grained annotations for each token


As previously stated, the annotation has been conducted on a global and a more fine-grained level.

The tagset used for the global and the fine-grained named entities is the following:

- Address
    - Building
    - City
    - Country
    - Place
    - Postcode
    - Street
    - Territory
- Amount
    - Unit
    - Value
- Date
    - Year
    - Standard Abbreviation
    - Month
    - Day of the Week
    - Day
    - Calender Event
- Person
    - Age
    - Email
    - Ethnic Category
    - Family Name
    - Financial
    - Given Name – Female
    - Given Name – Male
    - Health Insurance Number
    - ID Document Number
    - Initial Name
    - Marital Status
    - Medical Record Number
    - Nationality
    - Profession
    - Role
    - Social Security Number
    - Title
    - Url
- Organisation
- Time
- Vehicle
    - Build Year
    - Colour
    - License Plate Number
    - Model
    - Type

The final coarse grained tagset (in IOB notation) is the following: 

`['O', 'B-ORGANISATION', 'I-ORGANISATION', 'B-ADDRESS', 'I-ADDRESS', 'B-DATE', 'I-DATE', 'B-PERSON', 'I-PERSON', 'B-AMOUNT', 'I-AMOUNT', 'B-TIME', 'I-TIME']`


The final fine grained tagset (in IOB notation) is the following: 

`[
        'o',
        'b-day',
        'i-day',
        'b-month',
        'i-month',
        'b-year',
        'i-year',
        'b-title',
        'i-title',
        'b-family name',
        'i-family name',
        'b-initial name',
        'i-initial name',
        'b-age',
        'i-age',
        'b-value',
        'i-value',
        'b-unit',
        'i-unit',
        'b-country',
        'i-country',
        'b-city',
        'i-city',
        'b-place',
        'i-place',
        'b-territory',
        'i-territory',
        'b-role',
        'i-role',
        'b-profession',
        'i-profession',
        'b-marital status',
        'i-marital status',
        'b-url',
        'i-url',
        'b-ethnic category',
        'i-ethnic category',
        'b-standard abbreviation',
        'i-standard abbreviation'
        'b-type',
        'i-type',
        'b-building',
        'i-building',
        'b-nationality',
        'i-nationality',
]`


### Data Splits

Splits created by Joel Niklaus.


| language   |   # train files |   # validation files |   # test files |   # train sentences |   # validation sentences |   # test sentences |
|:-----------|----------------:|---------------------:|---------------:|--------------------:|-------------------------:|-------------------:|
| bg         |               9 |                    1 |              2 |                1411 |                      166 |                560 |
| cs         |               9 |                    1 |              2 |                1464 |                      176 |                563 |
| da         |               9 |                    1 |              2 |                1455 |                      164 |                550 |
| de         |               9 |                    1 |              2 |                1457 |                      166 |                558 |
| el         |               9 |                    1 |              2 |                1529 |                      174 |                584 |
| en         |               9 |                    1 |              2 |                 893 |                       98 |                408 |
| es         |               7 |                    1 |              1 |                 806 |                      248 |                155 |
| et         |               9 |                    1 |              2 |                1391 |                      163 |                516 |
| fi         |               9 |                    1 |              2 |                1398 |                      187 |                531 |
| fr         |               9 |                    1 |              2 |                1297 |                       97 |                490 |
| ga         |               9 |                    1 |              2 |                1383 |                      165 |                515 |
| hu         |               9 |                    1 |              2 |                1390 |                      171 |                525 |
| it         |               9 |                    1 |              2 |                1411 |                      162 |                550 |
| lt         |               9 |                    1 |              2 |                1413 |                      173 |                548 |
| lv         |               9 |                    1 |              2 |                1383 |                      167 |                553 |
| mt         |               9 |                    1 |              2 |                 937 |                       93 |                442 |
| nl         |               9 |                    1 |              2 |                1391 |                      164 |                530 |
| pt         |               9 |                    1 |              2 |                1086 |                      105 |                390 |
| ro         |               9 |                    1 |              2 |                1480 |                      175 |                557 |
| sk         |               9 |                    1 |              2 |                1395 |                      165 |                526 |
| sv         |               9 |                    1 |              2 |                1453 |                      175 |                539 |

## Dataset Creation

### Curation Rationale

*„[…] to our knowledge, there exist no open resources annotated for NERC [Named Entity Recognition and Classificatio] in Spanish in the legal domain. With the
present contribution, we intend to fill this gap. With the release of the created resources for fine-tuning and
evaluation of sensitive entities detection in the legal domain, we expect to encourage the development of domain-adapted
anonymisation tools for Spanish in this field“* (de Gibert Bonet et al., 2022)

### Source Data

#### Initial Data Collection and Normalization

The dataset consists of documents taken from EUR-Lex corpus which is publicly available. No further
information on the data collection process are given in de Gibert Bonet et al. (2022).

#### Who are the source language producers?

The source language producers are presumably lawyers.

### Annotations

#### Annotation process

*"The annotation scheme consists of a complex two level hierarchy adapted to the legal domain, it follows the scheme
described in (Gianola et al., 2020) […] Level 1 entities refer to general categories (PERSON, DATE, TIME, ADDRESS...)
and level 2 entities refer to more fine-grained subcategories (given name, personal name, day, year, month...). Eur-Lex,
CPP and DE have been annotated following this annotation scheme […] The manual annotation was performed using
INCePTION (Klie et al., 2018) by a sole annotator following the guidelines provided by the MAPA consortium."* (de Gibert
Bonet et al., 2022)

#### Who are the annotators?

Only one annotator conducted the annotation. More information are not provdided in de Gibert Bonet et al. (2022).

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

Note that the dataset at hand presents only a small portion of a bigger corpus as described in de Gibert Bonet et al. 
(2022). At the time of writing only the annotated documents from the EUR-Lex corpus were available.

Note that the information given in this dataset card refer to the dataset version as provided by Joel Niklaus and Veton
Matoshi. The dataset at hand is intended to be part of a bigger benchmark dataset. Creating a benchmark dataset
consisting of several other datasets from different sources requires postprocessing. Therefore, the structure of the
dataset at hand, including the folder structure, may differ considerably from the original dataset. In addition to that,
differences with regard to dataset statistics as give in the respective papers can be expected. The reader is advised to
have a look at the conversion script ```convert_to_hf_dataset.py``` in order to retrace the steps for converting the
original dataset into the present jsonl-format. For further information on the original dataset structure, we refer to
the bibliographical references and the original Github repositories and/or web pages provided in this dataset card.

## Additional Information

### Dataset Curators

The names of the original dataset curators and creators can be found in references given below, in the section *Citation
Information*. Additional changes were made by Joel Niklaus ([Email](joel.niklaus.2@bfh.ch)
; [Github](https://github.com/joelniklaus)) and Veton Matoshi ([Email](veton.matoshi@bfh.ch)
; [Github](https://github.com/kapllan)).

### Licensing Information

[Attribution 4.0 International (CC BY 4.0) ](https://creativecommons.org/licenses/by/4.0/)

### Citation Information

```
@article{DeGibertBonet2022,
author = {{de Gibert Bonet}, Ona and {Garc{\'{i}}a Pablos}, Aitor and Cuadros, Montse and Melero, Maite},
journal = {Proceedings of the Language Resources and Evaluation Conference},
number = {June},
pages = {3751--3760},
title = {{Spanish Datasets for Sensitive Entity Detection in the Legal Domain}},
url = {https://aclanthology.org/2022.lrec-1.400},
year = {2022}
}
```

### Contributions

Thanks to [@JoelNiklaus](https://github.com/joelniklaus) and [@kapllan](https://github.com/kapllan) for adding this
dataset.
