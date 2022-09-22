---
annotations_creators:
- other
language_creators:
- found
language:
- el
license:
- cc-by-nc-sa-4.0
multilinguality:
- monolingual
paperswithcode_id: null
pretty_name: Greek Legal Named Entity Recognition
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- token-classification
task_ids:
- named-entity-recognition
---

# Dataset Card for Greek Legal Named Entity Recognition

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
- **Point of Contact:** [Ilias Chalkidis](mailto:ilias.chalkidis@di.ku.dk); [Joel Niklaus](mailto:joel.niklaus.2@bfh.ch)

### Dataset Summary

This dataset contains an annotated corpus for named entity recognition in Greek legislations. It is the first of its kind for the Greek language in such an extended form and one of the few that examines legal text in a full spectrum entity recognition.

### Supported Tasks and Leaderboards

The dataset supports the task of named entity recognition.

### Languages

The language in the dataset is Greek as it used in the Greek Government Gazette.

## Dataset Structure

### Data Instances

The file format is jsonl and three data splits are present (train, validation and test).

### Data Fields

The files contain the following data fields
- `date`: The date when the document was published.
- `gazette`: The government gazette of the document. Either `A` or `D`
  - `A` is the general one, publishing standard legislation
  - `D` is meant for legislation on urban planning and such things
- `words`: The list of tokens obtained by applying the spacy (v 3.3.1) Greek tokenizer on the sentences. For more information see `convert_to_hf_dataset.py`.  
- `ner`: The list of ner tags. The list of labels for the named entities that are covered by the dataset are the following:
    - `FACILITY`: Facilities, such as police stations, departments etc.
    - `GPE`: Geopolitical Entity; any reference to a geopolitical entity (e.g., country, city, Greek administrative unit, etc.)
    - `LEG-REFS`: Legislation Reference; any reference to Greek or European legislation (e.g., Presidential Decrees, Laws, Decisions, EU Regulations and Directives, etc.)
    - `LOCATION-NAT`: Well defined natural location, such as rivers, mountains, lakes etc.
    - `LOCATION-UNK`: Poorly defined locations such "End of road X" or other locations that are not "official".
    - `ORG`: Organization; any reference to a public or private organization, such as: international organizations (e.g., European Union, United Nations, etc.), Greek public organizations (e.g., Social Insurance Institution) or private ones (e.g., companies, NGOs, etc.).
    - `PERSON`: Any formal name of a person mentioned in the text (e.g., Greek government members, public administration officials, etc.).
    - `PUBLIC-DOCS`: Public Document Reference; any reference to documents or decisions that have been published by a public institution (organization) that are not considered a primary source of legislation (e.g., local decisions, announcements, memorandums, directives).
    - `O`: No entity annotation present

The final tagset (in IOB notation) is the following: `['O', 'B-ORG', 'I-ORG', 'B-GPE', 'I-GPE', 'B-LEG-REFS', 'I-LEG-REFS', 'B-PUBLIC-DOCS', 'I-PUBLIC-DOCS', 'B-PERSON', 'I-PERSON', 'B-FACILITY', 'I-FACILITY', 'B-LOCATION-UNK', 'I-LOCATION-UNK', 'B-LOCATION-NAT', 'I-LOCATION-NAT']`

### Data Splits

The dataset has three splits: *train*, *validation* and *test*.

Split across the documents:

| split          | number of documents |
|:---------------|--------------------:|
| train          |               23723 |
| validation     |                5478 |
| test           |                5084 |

Split across NER labels

| NER label + split                              |   number of instances |
|:-----------------------------------------------|----------------------:|
| ('FACILITY', 'test')                           |                   142 |
| ('FACILITY', 'train')                          |                  1224 |
| ('FACILITY', 'validation')                     |                    60 |
| ('GPE', 'test')                                |                  1083 |
| ('GPE', 'train')                               |                  5400 |
| ('GPE', 'validation')                          |                  1214 |
| ('LEG-REFS', 'test')                           |                  1331 |
| ('LEG-REFS', 'train')                          |                  5159 |
| ('LEG-REFS', 'validation')                     |                  1382 |
| ('LOCATION-NAT', 'test')                       |                    26 |
| ('LOCATION-NAT', 'train')                      |                   145 |
| ('LOCATION-NAT', 'validation')                 |                     2 |
| ('LOCATION-UNK', 'test')                       |                   205 |
| ('LOCATION-UNK', 'train')                      |                  1316 |
| ('LOCATION-UNK', 'validation')                 |                   283 |
| ('ORG', 'test')                                |                  1354 |
| ('ORG', 'train')                               |                  5906 |
| ('ORG', 'validation')                          |                  1506 |
| ('PERSON', 'test')                             |                   491 |
| ('PERSON', 'train')                            |                  1921 |
| ('PERSON', 'validation')                       |                   475 |
| ('PUBLIC-DOCS', 'test')                        |                   452 |
| ('PUBLIC-DOCS', 'train')                       |                  2652 |
| ('PUBLIC-DOCS', 'validation')                  |                   556 |



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

According to (Angelidis et al., 2018) the authors of the paper annotated the data: *"Our group annotated all of the above documents for the 6 entity types that we examine."*

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

Note that the information given in this dataset card refer to the dataset version as provided by Joel Niklaus and Veton Matoshi. The dataset at hand is intended to be part of a bigger benchmark dataset. Creating a benchmark dataset consisting of several other datasets from different sources requires postprocessing. Therefore, the structure of the dataset at hand, including the folder structure, may differ considerably from the original dataset. In addition to that, differences with regard to dataset statistics as give in the respective papers can be expected. The reader is advised to have a look at the conversion script ```convert_to_hf_dataset.py``` in order to retrace the steps for converting the original dataset into the present jsonl-format. For further information on the original dataset structure, we refer to the bibliographical references and the original Github repositories and/or web pages provided in this dataset card.

## Additional Information

### Dataset Curators

The names of the original dataset curators and creators can be found in references given below, in the section *Citation Information*.
Additional changes were made by Joel Niklaus ([Email](mailto:joel.niklaus.2@bfh.ch); [Github](https://github.com/joelniklaus)) and Veton Matoshi ([Email](mailto:veton.matoshi@bfh.ch); [Github](https://github.com/kapllan)).


### Licensing Information

[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/)

### Citation Information

```
@inproceedings{Angelidis2018NamedER,
  author = {Angelidis, Iosif and Chalkidis, Ilias and Koubarakis, Manolis},
  booktitle = {JURIX},
  keywords = {greek,legal nlp,named entity recognition},
  title = {{Named Entity Recognition, Linking and Generation for Greek Legislation}},
  year = {2018}
}
```

### Contributions

Thanks to [@JoelNiklaus](https://github.com/joelniklaus) and [@kapllan](https://github.com/kapllan) for adding this dataset.
