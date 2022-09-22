---
annotations_creators:
- other
language_creators:
- found
language:
- ro
license:
- cc-by-nc-nd-4.0
multilinguality:
- monolingual
paperswithcode_id: null
pretty_name: Romanian Named Entity Recognition in the Legal domain (LegalNERo)
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- token-classification
task_ids:
- named-entity-recognition
---

# Dataset Card for Romanian Named Entity Recognition in the Legal domain (LegalNERo)

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
- **Repository:** https://zenodo.org/record/4922385
- **Paper:** Pais, V., Mitrofan, M., Gasan, C. L., Coneschi, V., & Ianov, A. (2021). Named Entity Recognition in the {R}omanian Legal Domain. Proceedings of the Natural Legal Language Processing Workshop 2021, 9–18. https://doi.org/10.18653/v1/2021.nllp-1.2
- **Leaderboard:**
- **Point of Contact:** [Joel Niklaus](mailto:joel.niklaus.2@bfh.ch)

### Dataset Summary

LegalNERo is a manually annotated corpus for named entity recognition in the Romanian legal domain. It provides gold annotations for organizations, locations, persons, time and legal resources mentioned in legal documents. Additionally it offers GEONAMES codes for the named entities annotated as location (where a link could be established).

### Supported Tasks and Leaderboards

The dataset supports the task of named entity recognition.

### Languages

Since legal documents for LegalNERo are extracted from the larger [MARCELL-RO corpus](https://elrc-share.eu/repository/browse/marcell-romanian-legislative-subcorpus-v2/2da548428b9d11eb9c1a00155d026706ce94a6b59ffc4b0e9fb5cd9cebe6889e/), the language in the dataset is Romanian as it used in national legislation ranging from 1881 to 2021.

## Dataset Structure

### Data Instances

The file format is jsonl and three data splits are present (train, validation and test). Named Entity annotations are non-overlapping.

Rows only containing one word (mostly words such as `\t\t\t`, `\n` or `-----`) have been filtered out.

### Data Fields

The files contain the following data fields
- `file_name`: The file_name of the applicable annotation document
- `words`: The list of tokens obtained by applying the spacy (v 3.3.1) Greek tokenizer on the sentences. For more information see `convert_to_hf_dataset.py`.  
- `ner`: The list of ner tags. The list of labels for the named entities that are covered by the dataset are the following:
    - `LEGAL`: Legal reference/resources 
    - `LOC`: Location
    - `ORG`: Organization
    - `PER`: Person
    - `TIME`: Time reference
    - `O`: No entity annotation present

The final tagset (in IOB notation) is the following: `['O', 'B-TIME', 'I-TIME', 'B-LEGAL', 'I-LEGAL', 'B-ORG', 'I-ORG', 'B-LOC', 'I-LOC', 'B-PER', 'I-PER']`

### Data Splits

Splits created by Joel Niklaus. 


| split          | number of documents | number of sentences |
|:---------------|--------------------:|--------------------:|
| train          |           296 (80%) |                7552 |
| validation     |            37 (10%) |                 966 |
| test           |            37 (10%) |                 907 |

## Dataset Creation

### Curation Rationale

The dataset provides gold annotations for organizations, locations, persons, time and legal resources mentioned in Romanian legal documents.

### Source Data

#### Initial Data Collection and Normalization

The LegalNERo corpus consists of 370 documents from the larger [MARCELL-RO corpus](https://elrc-share.eu/repository/browse/marcell-romanian-legislative-subcorpus-v2/2da548428b9d11eb9c1a00155d026706ce94a6b59ffc4b0e9fb5cd9cebe6889e/). In the following we give a short description of the crawling process for the MARCELL-RO corpus.

*The MARCELL-RO corpus "contains 163,274 files, which represent the body of national legislation ranging from 1881 to 2021. This corpus includes mainly: governmental decisions, ministerial orders, decisions, decrees and laws. All the texts were obtained via crawling from the public Romanian legislative portal . We have not distinguished between in force and "out of force" laws because it is difficult to do this automatically and there is no external resource to use to distinguish between them. The texts were extracted from the original HTML format and converted into TXT files. Each file has multiple levels of annotation: firstly the texts were tokenized, lemmatized and morphologically annotated using the Tokenizing, Tagging and Lemmatizing (TTL) text processing platform developed at RACAI, then dependency parsed with NLP-Cube, named entities were identified using a NER tool developed at RACAI, nominal phrases were identified also with TTL, while IATE terms and EuroVoc descriptors were identified using an internal tool. All processing tools were integrated into an end-to-end pipeline available within the RELATE platform and as a dockerized version. The files were annotated with the latest version of the pipeline completed within Activity 4 of the MARCELL project."* [Link](https://elrc-share.eu/repository/browse/marcell-romanian-legislative-subcorpus-v2/2da548428b9d11eb9c1a00155d026706ce94a6b59ffc4b0e9fb5cd9cebe6889e/)

#### Who are the source language producers?

The source language producers are presumably politicians and lawyers.

### Annotations

#### Annotation process

*“Annotation of the LegalNERo corpus was performed by 5 human annotators, supervised by two senior researchers at the Institute for Artificial Intelligence "Mihai Drăgănescu" of the Romanian Academy (RACAI). For annotation purposes we used the BRAT tool4 […].
Inside the legal reference class, we considered sub-entities of type *organization* and *time*. This allows for using the LegalNERo corpus in two scenarios: using all the 5 entity classes or using only the remaining general-purpose classes. The LegalNERo corpus contains a total of 370 documents from the larger MARCELL-RO corpus. These documents were split amongst the 5 annotators, with certain documents being annotated by multiple annotators. Each annotator manually annotated 100 documents. The annotators were unaware of the overlap, which allowed us to compute an inter-annotator agreement. We used the Cohen’s Kappa measure and obtained a value of 0.89, which we consider to be a good result.”* (Pais et al., 2021)


#### Who are the annotators?

*"[...] 5 human annotators, supervised by two senior researchers at the Institute for Artificial Intelligence "Mihai Drăgănescu" of the Romanian Academy (RACAI)."*

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

[Creative Commons Attribution Non Commercial No Derivatives 4.0 International](https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode)

### Citation Information

```
@dataset{pais_vasile_2021_4922385,
  author       = {Păiș, Vasile and
                  Mitrofan, Maria and
                  Gasan, Carol Luca and
                  Ianov, Alexandru and
                  Ghiță, Corvin and
                  Coneschi, Vlad Silviu and
                  Onuț, Andrei},
  title        = {{Romanian Named Entity Recognition in the Legal 
                   domain (LegalNERo)}},
  month        = may,
  year         = 2021,
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.4922385},
  url          = {https://doi.org/10.5281/zenodo.4922385}
}
```
```
@inproceedings{pais-etal-2021-named,
  author = {Pais, Vasile and Mitrofan, Maria and Gasan, Carol Luca and Coneschi, Vlad and Ianov, Alexandru},
  booktitle = {Proceedings of the Natural Legal Language Processing Workshop 2021},
  doi = {10.18653/v1/2021.nllp-1.2},
  month = {nov},
  pages = {9--18},
  publisher = {Association for Computational Linguistics},
  title = {{Named Entity Recognition in the {R}omanian Legal Domain}},
  url = {https://aclanthology.org/2021.nllp-1.2},
  year = {2021}
}
```

### Contributions

Thanks to [@JoelNiklaus](https://github.com/joelniklaus) and [@kapllan](https://github.com/kapllan) for adding this dataset.
