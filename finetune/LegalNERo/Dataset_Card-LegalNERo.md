---
TODO: Add YAML tags here. Copy-paste the tags obtained with the online tagging app: https://huggingface.co/spaces/huggingface/datasets-tagging
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

- **Homepage:** https://zenodo.org/record/4922385
- **Repository:** https://zenodo.org/record/4922385
- **Paper:** Pais, V., Mitrofan, M., Gasan, C. L., Coneschi, V., & Ianov, A. (2021). Named Entity Recognition in the {R}omanian Legal Domain. Proceedings of the Natural Legal Language Processing Workshop 2021, 9–18. https://doi.org/10.18653/v1/2021.nllp-1.2
- **Leaderboard:**
- **Point of Contact:** [Joel Niklaus](joel.niklaus.2@bfh.ch)

### Dataset Summary

LegalNERo is a manually annotated corpus for named entity recognition in the Romanian legal domain. It provides gold annotations for organizations, locations, persons, time and legal resources mentioned in legal documents. Additionally it offers GEONAMES codes for the named entities annotated as location (where a link could be established)

### Supported Tasks and Leaderboards

The dataset supports the task of named entity recognition.

### Languages

Since legal documents for LegalNERo are extracted from the larger [MARCELL-RO corpus](https://elrc-share.eu/repository/browse/marcell-romanian-legislative-subcorpus-v2/2da548428b9d11eb9c1a00155d026706ce94a6b59ffc4b0e9fb5cd9cebe6889e/), the language in the dataset is Romanian as it used in national legislation ranging from 1881 to 2021.

## Dataset Structure

### Data Instances

The LegalNERo corpus is available in different formats: span-based, token-based and RDF. 
The Linguistic Linked Open Data (LLOD) version is provided in RDF-Turtle format.

CONLLUP files conform to the CoNLL-U Plus format https://universaldependencies.org/ext-format.html .
Part-of-speech tagging was realized using UDPIPE. 
Named entity annotations are placed in the column "RELATE:NE" (the 11th column) as defined in the "global.columns" metadata field.
Similarly GEONAMES references are in the column "RELATE:GEONAMES" (the 12th column, last).
Automatic processing was performed through the RELATE platform (https://relate.racai.ro).

ANN files conform to BRAT format (https://brat.nlplab.org/).
 
The archive contains: 

- ann_LEGAL_PER_LOC_ORG_TIME_overlap:
    Folder in which all the files are in .ann format and contains annotations of: legal resources mentioned, persons, locations, organizations and time. 
    Overlapping annotations of organizations and time entities inside legal references were allowed. The statistics in (Pais et al., 2021) are based on the files in this folder.

- ann_LEGAL_PER_LOC_ORG_TIME: 
    Folder in which all the files are in .ann format and contains annotations of: legal resources mentioned, persons, locations, organizations and time. 
    Overlapping annotations were not allowed and only the longest named entities were annotated. 

- ann_PER_LOC_ORG_TIME: 
    Folder in which all the files are in .ann format and contains annotations of: persons, locations, organizations and time. 
    There are no overlapping annotations. 

- conllup_LEGAL_PER_LOC_ORG_TIME: 
    Folder in which all the files are in .conllup format and contains annotations of: legal resources mentioned, persons, locations, organizations and time. 
    Overlapping annotations were not allowed and only the longest named entities were annotated. 
    The annotation of these files was enhanced with GEONAMES codes (where linking was possible).  

- conllup_PER_LOC_ORG_TIME: 
    Folder in which all the files are in .conllup format and contains annotations of: persons, locations, organizations and time. 
    Overlapping annotations were not allowed and only the longest named entities were annotated. 
    The annotation of these files was enhanced with GEONAMES codes (where linking was possible).

- rdf 
    Folder containing the corpus in RDF-Turtle format.
    All the annotations are available here in both span and token format.

- text 
    Folder containing the raw texts.

### Data Fields

Below, we present the relevant fields for the .ann-files.

The main data fields in the ann-file are tab-seperated and the following:
- `ID`: The id of the annotation of the text
- `entity information`: This field is seperated by spaces and contains the following information:
  - `LABEL`: The annotation class (the class that entity was classified as). The list of labels for the named entities that are covered by the dataset are the following:
    - `LEGAL`: Legal reference/resources 
    - `LOC`: Location
    - `ORG`: Organization
    - `PER`: Person
    - `TIME`: Time reference

### Data Splits

No split provided.

## Dataset Creation

### Curation Rationale

The dataset provides gold annotations for organizations, locations, persons, time and legal resources mentioned in legal documents.

### Source Data

#### Initial Data Collection and Normalization

The LegalNERo corpus consists of 370 documents from the larger [MARCELL-RO corpus](https://elrc-share.eu/repository/browse/marcell-romanian-legislative-subcorpus-v2/2da548428b9d11eb9c1a00155d026706ce94a6b59ffc4b0e9fb5cd9cebe6889e/).

*The MARCELL-RO corpus "contains 163,274 files, which represent the body of national legislation ranging from 1881 to 2021. This corpus includes mainly: governmental decisions, ministerial orders, decisions, decrees and laws. All the texts were obtained via crawling from the public Romanian legislative portal . We have not distinguished between in force and "out of force" laws because it is difficult to do this automatically and there is no external resource to use to distinguish between them. The texts were extracted from the original HTML format and converted into TXT files. Each file has multiple levels of annotation: firstly the texts were tokenized, lemmatized and morphologically annotated using the Tokenizing, Tagging and Lemmatizing (TTL) text processing platform developed at RACAI, then dependency parsed with NLP-Cube, named entities were identified using a NER tool developed at RACAI, nominal phrases were identified also with TTL, while IATE terms and EuroVoc descriptors were identified using an internal tool. All processing tools were integrated into an end-to-end pipeline available within the RELATE platform and as a dockerized version. The files were annotated with the latest version of the pipeline completed within Activity 4 of the MARCELL project."* [Link](https://elrc-share.eu/repository/browse/marcell-romanian-legislative-subcorpus-v2/2da548428b9d11eb9c1a00155d026706ce94a6b59ffc4b0e9fb5cd9cebe6889e/)

#### Who are the source language producers?

[More Information Needed]

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

[More Information Needed]

## Additional Information

### Dataset Curators

(Pais et al., 2021)

### Licensing Information

[Creative Commons Attribution Non Commercial No Derivatives 4.0 International](https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode)

### Citation Information

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

@inproceedings{pais-etal-2021-named,
  abstract = {Recognition of named entities present in text is an important step towards information extraction and natural language understanding. This work presents a named entity recognition system for the Romanian legal domain. The system makes use of the gold annotated LegalNERo corpus. Furthermore, the system combines multiple distributional representations of words, including word embeddings trained on a large legal domain corpus. All the resources, including the corpus, model and word embeddings are open sourced. Finally, the best system is available for direct usage in the RELATE platform.},
  address = {Punta Cana, Dominican Republic},
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

### Contributions

Thanks to [@JoelNiklaus](https://github.com/joelniklaus) and [@kapllan](https://github.com/kapllan) for adding this dataset.
