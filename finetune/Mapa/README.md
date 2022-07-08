---
annotations_creators:
- other
language_creators:
- found
languages:
- es
license:
- CC-BY-4.0
multilinguality:
- monolingual
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

# Dataset Card for Spanish Datasets for Sensitive Entity Detection in the Legal Domain

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
  Repository:** https://elrc-share.eu/repository/browse/mapa-anonymization-package-spanish/b550e1a88a8311ec9c1a00155d026706687917f92f64482587c6382175dffd76/
- **Paper:** de Gibert Bonet, O., García Pablos, A., Cuadros, M., & Melero, M. (2022). Spanish Datasets for Sensitive
  Entity Detection in the Legal Domain. Proceedings of the Language Resources and Evaluation Conference, June,
  3751–3760. http://www.lrec-conf.org/proceedings/lrec2022/pdf/2022.lrec-1.400.pdf
- **Leaderboard:**
- **Point of Contact:** [Joel Niklaus](joel.niklaus.2@bfh.ch)

### Dataset Summary

The dataset consists of 12 documents (2261 sentences) in Spanish taken from EUR-Lex, a multilingual corpus of court
decisions and legal dispositions in the 24 official languages of the European Union. The documents have been annotated
for named entities following the guidelines of the [MAPA project]( https://mapa-project.eu/) which foresees two
annotation level, a general and a more fine-grained one. The annotated corpus can be used for named entity recognition/
classification.

### Supported Tasks and Leaderboards

The dataset supports the task of named entity recognition or, as de Gibert Bonet et al. (2022) state, named entity
recognition and classification (NERC).

### Languages

The language in the dataset is Spanish as it used in European court decisions and legal dispositions.

## Dataset Structure

### Data Instances

The format of the annotated data is webanno tsv 3.2. Each annotated document is saved as a tsv file. The original
dataset does not provide train-test-split.

### Data Fields

The annotations have been done on the sentence level. For each sentence the following data fields or columns are
provided:

- `id`: It consists of combination of the sentence id and the token id.
- `span`:  Provides the start and end id of the token in the row.
- `token`: Token of the document.
- `abstract representation of entities`: If a token is not part of a named entity the field remains blank. If a token is
  part of a named entity, the existence of the named is indicated by an asterisk followed by an id in brackets. In case
  for one and the same token two named entities were annotated, one for the global category and one for the more
  fine-grained category, the two named entities are separated by a pipe. - Example for cases with an annotation only on
  the global level: *[1]
    - Example for cases with an annotation on the global level and the fine-grained level: \*[2]|*[3]
- `named entity tag`: The annotation scheme corresponds the previous field, except that instead of the asterisk the
  actual tag for the named entity is provided. - Example for cases with an annotation only on the global level:
  ORGANISATION[1]
    - Example for cases with an annotation on the global level and the fine-grained level: country[2]|ADDRESS[3]

As previously stated, the annotation has been conducted on a global or abstract and a more fine-grained level.

The tags used for the global and the fine-grained named entity categories are:

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
    - Ttitle
    - Url
- Organisation
- Time
- Vehicle
    - Build Year
    - Colour
    - License Plate Number
    - Model
    - Type

### Data Splits

Splits created by Joel Niklaus.

## Dataset Creation

### Curation Rationale

*„[…] to our knowledge, there exist no open resources annotated for NERC in Spanish in the legal domain. With the
present contribution, we intend to fill this gap. With the release of the created resources for fine-tuning and
evaluation of sensitive entities detection in the legal domain, we expect to encourage the development of domain-adapted
anonymisation tools for Spanish in this field“* (de Gibert Bonet et al., 2022)

### Source Data

#### Initial Data Collection and Normalization

The dataset consists of documents in Spanish taken from EUR-Lex corpus which is publicly available. No further
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

Note that the dataset at hand presents only a small portion of a bigger corpus as described in de Gibert Bonet et al. (
2022). At the time of writing only the annotated documents from the EUR-Lex corpus were available.

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
