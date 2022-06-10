---
TODO: Add YAML tags here. Copy-paste the tags obtained with the online tagging app: https://huggingface.co/spaces/huggingface/datasets-tagging
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
- **Repository:** https://github.com/tommasoc80/COVID19_emergency_event; https://dataverse.nl/dataset.xhtml?persistentId=doi:10.34894/ZUWAPS
- **Paper:** Tziafas, G., de Saint-Phalle, E., de Vries, W., Egger, C., & Caselli, T. (2021). A Multilingual Approach to Identify and Classify Exceptional Measures against {COVID}-19. Proceedings of the Natural Legal Language Processing Workshop 2021, 46–62. https://doi.org/10.18653/v1/2021.nllp-1.5
- **Leaderboard:**
- **Point of Contact:** [Joel Niklaus](joel.niklaus.2@bfh.ch)

### Dataset Summary

This dataset presents a new corpus of legislative documents from 21 European countries manually annotated for exceptional measures against COVID-19. The annotation was done on the sentence level.

### Supported Tasks and Leaderboards

The dataset can be used for multi-label text classification tasks.

### Languages

Dutch, English, French, Hungarian, Italian, Norwegian Bokmål, Polish

## Dataset Structure

### Data Instances

The folder `/annotations/` contains the manually annotated data per country, already split in Train/Dev/Test. The folder contains a subfolder for each country, i.e. Beglium, France, Hunary, Italy, Netherlands, Norway, Poland, UK. Each subfolder contains tsv files with the annotated data. Besides that, the folder `/annotations/` contains the files *all_train_or.tsv*, *all_dev_or.tsv*, *all_test_or.tsv* that combine the train, dev and test data of each country.

### Data Fields

The tsv files have the following basic columns:
- `id`: Sentence id
- `text`: Sentence that has been annotated

The documents have been annotated with 8 labels, each label representing a specific measurement agains COVID-19. Each label is represented by one column in the tsv file. The labels, i.e. the specific measure classes, are:
- `event1`: State of Emergency
- `event2`: Restrictions of fundamental rights and civil liberties
- `event3`: Restrictions of daily liberties
- `event4`: Closures / lockdown 
- `event5`: Suspension of international cooperation and commitments
- `event6`: Police mobilization
- `event7`: Army mobilization 
- `event8`: Government oversight


### Data Splits

???? MY NUMBERS ARE THE FOLLOWING BUT THE PAPER HAS SLIGHTLY DIFFERENT NUMBERS:
- train:  3501
- dev:  442
- test:  442


## Dataset Creation

### Curation Rationale

*"Investigate the potential of multilingual pretrained language models in order to
facilitate the analysis, exploration, and comparison of legal texts on COVID-19 exceptional measures"* (Tziafas et al., 2021)

### Source Data

#### Initial Data Collection and Normalization

*“The corpus collection process has been overseen by four political science experts working in partnership with national legal experts. All documents were retrieved from official governmental websites that publish legal acts. The identification of the relevant documents has been done by means of 4 keywords (i.e., “COVID”, “COVID-19”, “Coronavirus” and “Health emergency”). For each language, the corresponding language specific keywords were used. In this initial phase, we focus on a sample of 19 EEA countries on measures adopted at the national level. To do so, we identify publicly available links to relevant documents 2 plus UK and Switzerland. We could not find corresponding documents for two countries of the EEA (i.e., Bulgaria and Greece). All documents have been collected either by manually downloading them or by automatic scraping.3 For countries with more than one official language (e.g., Switzerland), legal acts were collected in all available languages.”*(Tziafas et al., 2021)


#### Who are the source language producers?

[More Information Needed]

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

[More Information Needed]

## Additional Information

### Dataset Curators

[More Information Needed]

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
    abstract = "The COVID-19 pandemic has witnessed the implementations of exceptional measures by governments across the world to counteract its impact. This work presents the initial results of an on-going project, EXCEPTIUS, aiming to automatically identify, classify and com- pare exceptional measures against COVID-19 across 32 countries in Europe. To this goal, we created a corpus of legal documents with sentence-level annotations of eight different classes of exceptional measures that are im- plemented across these countries. We evalu- ated multiple multi-label classifiers on a manu- ally annotated corpus at sentence level. The XLM-RoBERTa model achieves highest per- formance on this multilingual multi-label clas- sification task, with a macro-average F1 score of 59.8{\%}.",
}
``` 

### Contributions

Thanks to [@JoelNiklaus](https://github.com/joelniklaus) and [@kapllan](https://github.com/kapllan) for adding this dataset.
