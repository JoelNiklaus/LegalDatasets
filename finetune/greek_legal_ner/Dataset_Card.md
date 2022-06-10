---
TODO: Add YAML tags here. Copy-paste the tags obtained with the online tagging app: https://huggingface.co/spaces/huggingface/datasets-tagging
---

# Dataset Card for Greek Legal Named Entity Recognition and Linking

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

- **Homepage:** http://legislation.di.uoa.gr/publications?language=en
- **Repository:** 
- **Paper:** Angelidis, I., Chalkidis, I., & Koubarakis, M. (2018). Named Entity Recognition, Linking and Generation for Greek Legislation. JURIX.
- **Leaderboard:** 
- **Point of Contact:** [Ilias Chalkidis](ilias.chalkidis@di.ku.dk); [Joel Niklaus](joel.niklaus.2@bfh.ch)

### Dataset Summary

*"The benchmark datasets contain 254 daily issues for classes A and D of the Greek Government Gazette over the period 2000-2017. Every issue contains multiple legal acts. Class A issues concern primary legislation published by the Greek government (e.g., laws, presidential decrees, ministerial decisions, regulations, etc.). Class D issues concern decisions related to urban, rural and environmental planning (e.g., reforestations, declassifications, expropriations, etc.). We uniformly splitted the issues across training (162), validation (45), and test (47) in terms of publication year and class. Thus the possibility of overfitting due to specific linguistic idiosyncrasies in the language of a government or due to specific entities and policies has been minimized. Our group annotated all of the above documents for the 6 entity types that we examine. We also created datasets that contain pairs of entity references and the respective matching Universal Resource Identifiers (URIs) in other open public datasets."* (Angelidis et al., 2018)

### Supported Tasks and Leaderboards

The dataset supports the task of named entity recognition.

### Languages

The language in the dataset is Greek as it used in the Greek Government Gazette.

## Dataset Structure

### Data Instances

The ENTITY RECOGNITION folder contains the annotated dataset we used to evaluate our NER component. It is already split into TEST, TRAIN and VALIDATION. Each of these folders contains the .txt (original document) and .ann (files with the annotations and offsets
they are found in the text) files .

### Data Fields

The main data fields in the ann-file are tab-seperated and the following:
- `ID`: The id of the annotation of the text
- `entity information`: This field is seperated by spaces and contains the following information:
  - `LABEL`: The annotation class (the class that entity was classified as). The list of labels for the named entities that are covered by the dataset are the following:
    - `FACILITY`: Facilities, such as police stations, departments etc.
    - `GPE`: Geopolitical Entity; any reference to a geopolitical entity (e.g., country, city, Greek administrative unit, etc.)
    - `LEG-REFS`: Legislation Reference; any reference to Greek or European legislation (e.g., Presidential Decrees, Laws, Decisions, EU Regulations and Directives, etc.)
    - `LOCATION-NAT`: Natural location, such as rivers, mountains, lakes etc.
    - `LOCATION-UNK`: ???? 
    - `ORG`: Organization; any reference to a public or private organization, such as: international organizations (e.g., European Union, United Nations, etc.), Greek public organizations (e.g., Social Insurance Institution) or private ones (e.g., companies, NGOs, etc.).
    - `PERSON`: Any formal name of a person mentioned in the text (e.g., Greek government members, public administration officials, etc.).
    - `PUBLIC-DOCS`: Public Document Reference; any reference to documents or decisions that have been published by a public institution (organization) that are not considered a primary source of legislation (e.g., local decisions, announcements, memorandums, directives).
  - `START`: index of the character within a document where the respective named entity starts.
  - `END`: index of the character within a document where the respective named entity ends.
- `STRING`: Span within the document that represents the named entity.

### Data Splits

The dataset has three splits: *train*, *validation* and *test*.

- Split accross the documents:

| split   |   number of documents |
|:-----------------|-------:|
| test             |   5084 |
| train            |  23723 |
| validation       |   5478 |

- Split accross NER labels

| NER label + split                               |   number of instances |
|:-------------------------------|-------:|
| ('FACILITY', 'test')           |    142 |
| ('FACILITY', 'train')          |   1224 |
| ('FACILITY', 'validation')     |     60 |
| ('GPE', 'test')                |   1083 |
| ('GPE', 'train')               |   5400 |
| ('GPE', 'validation')          |   1214 |
| ('LEG-REFS', 'test')           |   1331 |
| ('LEG-REFS', 'train')          |   5159 |
| ('LEG-REFS', 'validation')     |   1382 |
| ('LOCATION-NAT', 'test')       |     26 |
| ('LOCATION-NAT', 'train')      |    145 |
| ('LOCATION-NAT', 'validation') |      2 |
| ('LOCATION-UNK', 'test')       |    205 |
| ('LOCATION-UNK', 'train')      |   1316 |
| ('LOCATION-UNK', 'validation') |    283 |
| ('ORG', 'test')                |   1354 |
| ('ORG', 'train')               |   5906 |
| ('ORG', 'validation')          |   1506 |
| ('PERSON', 'test')             |    491 |
| ('PERSON', 'train')            |   1921 |
| ('PERSON', 'validation')       |    475 |
| ('PUBLIC-DOCS', 'test')        |    452 |
| ('PUBLIC-DOCS', 'train')       |   2652 |
| ('PUBLIC-DOCS', 'validation')  |    556 |



## Dataset Creation

### Curation Rationale

Creating a big dataset for Greek named entity recognition and entity linking.

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

Greek Government Gazette

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

[Ilias Chalkidis](https://gitlab.com/ilias.chalkidis); [Iosif Angelidis](https://gitlab.com/metimdjai)

### Licensing Information

[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/)

### Citation Information

[More Information Needed]

### Contributions

Thanks to [@JoelNiklaus](https://github.com/joelniklaus) and [@kapllan](https://github.com/kapllan) for adding this dataset.
