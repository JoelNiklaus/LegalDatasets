---
annotations_creators:
- found
language_creators:
- found
language:
- pt
license:
- 'other'
multilinguality:
- monolingual
pretty_name: predicting-brazilian-court-decisions
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- multi-class-classification
---

# Dataset Card for predicting-brazilian-court-decisions

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
- **Repository:** https://github.com/lagefreitas/predicting-brazilian-court-decisions
- **Paper:** Lage-Freitas, A., Allende-Cid, H., Santana, O., & Oliveira-Lage, L. (2022). Predicting Brazilian Court
  Decisions. PeerJ. Computer Science, 8, e904–e904. https://doi.org/10.7717/peerj-cs.904
- **Leaderboard:**
- **Point of Contact:** [Joel Niklaus](mailto:joel.niklaus.2@bfh.ch)

### Dataset Summary

The dataset is a collection of 4043 *Ementa* (summary) court decisions and their metadata from
the *Tribunal de Justiça de Alagoas* (TJAL, the State Supreme Court of Alagoas (Brazil). The court decisions are labeled
according to 7 categories and whether the decisions were unanimous on the part of the judges or not. The dataset
supports the task of Legal Judgment Prediction.

### Supported Tasks and Leaderboards

Legal Judgment Prediction

### Languages

Brazilian Portuguese

## Dataset Structure

### Data Instances

The file format is jsonl and three data splits are present (train, validation and test) for each configuration.

### Data Fields

The dataset contains the following fields:

- `process_number`: A number assigned to the decision by the court
- `orgao_julgador`: Judging Body: one of '1ª Câmara Cível', '2ª Câmara Cível', '3ª Câmara Cível', 'Câmara Criminal', '
  Tribunal Pleno', 'Seção Especializada Cível'
- `publish_date`: The date, when the decision has been published (14/12/2018 - 03/04/2019). At that time (in 2018-2019),
  the scraping script was limited and not configurable to get data based on date range. Therefore, only the data from
  the last months has been scraped.
- `judge_relator`: Judicial panel
- `ementa_text`: Summary of the court decision
- `decision_description`: **Suggested input**. Corresponds to ementa_text - judgment_text - unanimity_text. Basic
  statistics (number of words): mean: 119, median: 88, min: 12, max: 1400
- `judgment_text`: The text used for determining the judgment label
- `judgment_label`: **Primary suggested label**. Labels that can be used to train a model for judgment prediction:
    - `no`: The appeal was denied
    - `partial`: For partially favourable decisions
    - `yes`: For fully favourable decisions
    - removed labels (present in the original dataset):
        - `conflito-competencia`: Meta-decision. For example, a decision just to tell that Court A should rule this case
          and not Court B.
        - `not-cognized`: The appeal was not accepted to be judged by the court
        - `prejudicada`: The case could not be judged for any impediment such as the appealer died or gave up on the
          case for instance.
- `unanimity_text`: Portuguese text to describe whether the decision was unanimous or not.
- `unanimity_label`: **Secondary suggested label**. Unified labels to describe whether the decision was unanimous or
  not (in some cases contains ```not_determined```); they can be used for model training as well  (Lage-Freitas et al.,
  2019).

### Data Splits

The data has been split randomly into 80% train (3234), 10% validation (404), 10% test (405).

There are two tasks possible for this dataset.

#### Judgment
Label Distribution

| judgment  |    train | validation |    test |
|:----------|---------:|-----------:|--------:|
| no        |     1960 |        221 |     234 |
| partial   |      677 |         96 |      93 |
| yes       |      597 |         87 |      78 |
| **total** | **3234** |    **404** | **405** |

#### Unanimity

In this configuration, all cases that have `not_determined` as `unanimity_label` can be removed.

Label Distribution

| unanimity_label  |     train |     validation |     test |
|:-----------------|----------:|---------------:|---------:|
| not_determined   |      1519 |            193 |      201 |
| unanimity        |      1681 |            205 |      200 |
| not-unanimity    |        34 |              6 |        4 |
| **total**        |  **3234** |        **404** |  **405** |

## Dataset Creation

### Curation Rationale

This dataset was created to further the research on developing models for predicting Brazilian court decisions that are
also able to predict whether the decision will be unanimous.

### Source Data

The data was scraped from *Tribunal de Justiça de Alagoas* (TJAL, the State Supreme Court of Alagoas (Brazil).

#### Initial Data Collection and Normalization

*“We developed a Web scraper for collecting data from Brazilian courts. The scraper first searched for the URL that
contains the list of court cases […]. Then, the scraper extracted from these HTML files the specific case URLs and
downloaded their data […]. Next, it extracted the metadata and the contents of legal cases and stored them in a CSV file
format […].”* (Lage-Freitas et al., 2022)

#### Who are the source language producers?

The source language producer are presumably attorneys, judges, and other legal professionals.

### Annotations

#### Annotation process

The dataset was not annotated.

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

The court decisions might contain sensitive information about individuals.

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

Note that the information given in this dataset card refer to the dataset version as provided by Joel Niklaus and Veton
Matoshi. The dataset at hand is intended to be part of a bigger benchmark dataset. Creating a benchmark dataset
consisting of several other datasets from different sources requires postprocessing. Therefore, the structure of the
dataset at hand, including the folder structure, may differ considerably from the original dataset. In addition to that,
differences with regard to dataset statistics as give in the respective papers can be expected. The reader is advised to
have a look at the conversion script ```convert_to_hf_dataset.py``` in order to retrace the steps for converting the
original dataset into the present jsonl-format. For further information on the original dataset structure, we refer to
the bibliographical references and the original Github repositories and/or web pages provided in this dataset card.

## Additional Information

Lage-Freitas, A., Allende-Cid, H., Santana Jr, O., & Oliveira-Lage, L. (2019). Predicting Brazilian court decisions:

- "In Brazil [...] lower court judges decisions might be appealed to Brazilian courts (*Tribiunais de Justiça*) to be
  reviewed by second instance court judges. In an appellate court, judges decide together upon a case and their
  decisions are compiled in Agreement reports named *Acóordãos*."

### Dataset Curators

The names of the original dataset curators and creators can be found in references given below, in the section *Citation
Information*. Additional changes were made by Joel Niklaus ([Email](mailto:joel.niklaus.2@bfh.ch)
; [Github](https://github.com/joelniklaus)) and Veton Matoshi ([Email](mailto:veton.matoshi@bfh.ch)
; [Github](https://github.com/kapllan)).

### Licensing Information

No licensing information was provided for this dataset. However, please make sure that you use the dataset according to
Brazilian law.

### Citation Information

```
@misc{https://doi.org/10.48550/arxiv.1905.10348,
  author = {Lage-Freitas, Andr{\'{e}} and Allende-Cid, H{\'{e}}ctor and Santana, Orivaldo and de Oliveira-Lage, L{\'{i}}via},
  doi = {10.48550/ARXIV.1905.10348},
  keywords = {Computation and Language (cs.CL),FOS: Computer and information sciences,Social and Information Networks (cs.SI)},
  publisher = {arXiv},
  title = {{Predicting Brazilian court decisions}},
  url = {https://arxiv.org/abs/1905.10348},
  year = {2019}
}
```

```
@article{Lage-Freitas2022,
  author = {Lage-Freitas, Andr{\'{e}} and Allende-Cid, H{\'{e}}ctor and Santana, Orivaldo and Oliveira-Lage, L{\'{i}}via},
  doi = {10.7717/peerj-cs.904},
  issn = {2376-5992},
  journal = {PeerJ. Computer science},
  keywords = {Artificial intelligence,Jurimetrics,Law,Legal,Legal NLP,Legal informatics,Legal outcome forecast,Litigation prediction,Machine learning,NLP,Portuguese,Predictive algorithms,judgement prediction},
  language = {eng},
  month = {mar},
  pages = {e904--e904},
  publisher = {PeerJ Inc.},
  title = {{Predicting Brazilian Court Decisions}},
  url = {https://pubmed.ncbi.nlm.nih.gov/35494851 https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9044329/},
  volume = {8},
  year = {2022}
}
```

### Contributions

Thanks to [@kapllan](https://github.com/kapllan) and [@joelniklaus](https://github.com/joelniklaus) for adding this
dataset.
