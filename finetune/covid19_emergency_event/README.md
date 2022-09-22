---
annotations_creators:
- found
- other
language_creators:
- found
language:
- en
- fr
- hu
- it
- nb
- nl
- pl
license:
- cc0-1.0
multilinguality:
- multilingual
pretty_name: EXCEPTIUS Corpus
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- multi-label-classification
---

# Dataset Card for EXCEPTIUS Corpus

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

- **Homepage:** https://exceptius.com/
- **Repository:** https://github.com/tommasoc80/COVID19_emergency_event
- **Paper:** Tziafas, G., de Saint-Phalle, E., de Vries, W., Egger, C., & Caselli, T. (2021). A Multilingual Approach to Identify and Classify Exceptional Measures against {COVID}-19. Proceedings of the Natural Legal Language Processing Workshop 2021, 46–62. https://doi.org/10.18653/v1/2021.nllp-1.5
- **Leaderboard:**
- **Point of Contact:** [Joel Niklaus](mailto:joel.niklaus.2@bfh.ch)

### Dataset Summary

This dataset presents a new corpus of legislative documents from 8 European countries (Beglium, France, Hunary, Italy, Netherlands, Norway, Poland, UK) in 7 languages (Dutch, English, French, Hungarian, Italian, Norwegian Bokmål, Polish) manually annotated for exceptional measures against COVID-19. The annotation was done on the sentence level.

### Supported Tasks and Leaderboards

The dataset can be used for multi-label text classification tasks.

### Languages

Dutch, English, French, Hungarian, Italian, Norwegian Bokmål, Polish

## Dataset Structure

### Data Instances

The file format is jsonl and three data splits are present (train, validation and test).

### Data Fields

The jsonl files have the following basic columns:
- `language`: The language of the sentence (set based on the country)
- `country`: The country of the sentence
- `text`: Sentence that has been annotated

The documents have been annotated with 8 labels, each label representing a specific measurement against COVID-19. Each label is represented by one boolean field in the jsonl file. The labels, i.e. the specific measure classes, are:
- `event1`: State of Emergency
- `event2`: Restrictions of fundamental rights and civil liberties
- `event3`: Restrictions of daily liberties
- `event4`: Closures / lockdown 
- `event5`: Suspension of international cooperation and commitments
- `event6`: Police mobilization
- `event7`: Army mobilization 
- `event8`: Government oversight
- `all_events`: an aggregate column containing all applicable events combined

### Data Splits

All annotated sentences combined have the following split:
- train: 3312 (80%)
- dev: 418 (10%)
- test: 418 (10%)

The splits have been performed on each country and have later been merged. Therefore, each split contains sentences from each country.

The following label distribution shows the number of occurrences per label per split. `total occurrences` sums up the previous rows (total number of events per split). `split size` is the number of sentences per split.

| Event                 |     train | validation |      test |
|:----------------------|----------:|-----------:|----------:|
| event1                |       383 |         54 |        47 |
| event2                |       253 |         39 |        42 |
| event3                |       412 |         70 |        62 |
| event4                |       617 |         75 |        93 |
| event5                |        52 |          4 |         6 |
| event6                |        15 |          2 |         1 |
| event7                |        45 |          4 |         5 |
| event8                |       146 |         21 |        19 |
| **total occurrences** |  **1923** |    **269** |   **275** |
| **split size**        |  **3312** |    **418** |   **418** |


## Dataset Creation

### Curation Rationale

*"Investigate the potential of multilingual pretrained language models in order to
facilitate the analysis, exploration, and comparison of legal texts on COVID-19 exceptional measures"* (Tziafas et al., 2021)

### Source Data

#### Initial Data Collection and Normalization

*“The corpus collection process has been overseen by four political science experts working in partnership with national legal experts. All documents were retrieved from official governmental websites that publish legal acts. The identification of the relevant documents has been done by means of 4 keywords (i.e., “COVID”, “COVID-19”, “Coronavirus” and “Health emergency”). For each language, the corresponding language specific keywords were used. In this initial phase, we focus on a sample of 19 EEA countries on measures adopted at the national level. To do so, we identify publicly available links to relevant documents 2 plus UK and Switzerland. We could not find corresponding documents for two countries of the EEA (i.e., Bulgaria and Greece). All documents have been collected either by manually downloading them or by automatic scraping. For countries with more than one official language (e.g., Switzerland), legal acts were collected in all available languages.”*(Tziafas et al., 2021)


#### Who are the source language producers?

Politicians and legal experts have been involved in producing the language material.

### Annotations

#### Annotation process

*"A subset of 281 documents in eight languages has been selected for manual annotation. The annotation of the exceptional measures applies at sentence-level. The sample is based on the French, Polish, Dutch, English, Hungarian, Belgian, Italian, and Norwegian sub-corpora. Annotators were allowed to assign as many subclasses as they consider relevant to each sentence, but with a total of eight main classes of exceptional measures. Sentences can potentially entail multiple exceptional classes, making this a multi-label annotation task. The annotation process results in eight binary annotations per sentence, with 0 if the specific class is not identified within the sentence and 1 if it is. The annotation has been conducted by three experts in political science working under the supervision of the project’s Scientific Board. Since the annotators are not fluent in all languages and due to the impossibility of recruiting expert native speakers, some documents need to be translated into English to be manually annotated. No inter-annotator agreement study has been conducted in this initial phase. We intend to remedy this limitation in the project’s next development cycle. However, during the annotation phase, annotators met on a weekly basis to discuss ambiguous cases and the guidelines. Annotators are encouraged to propose new classes or subclasses. For a new (sub)class to be accepted, the measure should have been independently identified by the majority of the annotators. In this phase, no new classes were proposed."* (Tziafas et al., 2021)

#### Who are the annotators?

*"The annotation has been conducted by three experts in political science working under the supervision of the project’s Scientific Board."* (Tziafas et al., 2021)

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

Creative Commons Zero v1.0 Universal

### Citation Information

```
@inproceedings{tziafas-etal-2021-multilingual,
    title = "A Multilingual Approach to Identify and Classify Exceptional Measures against {COVID}-19",
    author = "Tziafas, Georgios  and
      de Saint-Phalle, Eugenie  and
      de Vries, Wietse  and
      Egger, Clara  and
      Caselli, Tommaso",
    booktitle = "Proceedings of the Natural Legal Language Processing Workshop 2021",
    month = nov,
    year = "2021",
    address = "Punta Cana, Dominican Republic",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.nllp-1.5",
    pages = "46--62",
}
``` 

### Contributions

Thanks to [@JoelNiklaus](https://github.com/joelniklaus) and [@kapllan](https://github.com/kapllan) for adding this dataset.
