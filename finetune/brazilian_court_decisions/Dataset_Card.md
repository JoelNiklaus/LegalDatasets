---
annotations_creators:
- other
language_creators:
- other
languages:
- Portuguese
licenses:
- other-This dataset should be used according to Brazilian law
multilinguality:
- monolingual
pretty_name: predicting-brazilian-court-decisions
size_categories: []
source_datasets: []
task_categories:
- text-classification
task_ids:
- multi-label-classification
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
- **Paper:** André Lage-Freitas, Héctor Allende-Cid, Orivaldo Santana, and Lívia Oliveira-Lage. Predicting Brazilian court decisions. Technical Report. 2019.
- **Leaderboard:**
- **Point of Contact:** [Joel Niklaus](joel.niklaus.2@bfh.ch)

### Dataset Summary

The dataset is a collection of 9644 (9608 after our filters) *Ementa* (summary) court decisions and their metadata from the *Tribunal de Justiça de Alagoas* (TJAL, the State Supreme Court of Alagoas (Brazil). The court decisions are labeled according to 7 categories and whether the decisions were unanimous on the part of the judges or not. The dataset supports the task of Neural Legal Judgment Prediction.

### Supported Tasks and Leaderboards

Neural Legal Judgment Prediction

### Languages

Brazilian Portuguese

## Dataset Structure

### Data Instances
The file format is CSV and its separator (delimiter) is "<=>". The csv files contains 9644 (9608 after our filters) instances of court decisions and 14 columns (fields) with (meta-)information. 

### Data Fields

The dataset contains the following fields:
  - `process_number`: A number assigned to the decision by the court
  - `orgao_julgador`: Judging Body: one of '1ª Câmara Cível', '2ª Câmara Cível', '3ª Câmara Cível', 'Câmara Criminal', 'Tribunal Pleno', 'Seção Especializada Cível'
  - `publish_date`: The date, when the decision has been published (14/12/2018 - 03/04/2019)
  - `judge_relator`: Judicial panel
  - `ementa_text`: Summary of the court decision
  - `decision_description`: **Suggested input**. Corresponds to ementa_text - decision_text - decision_unanimity_text. Basic statistics (number of words): mean: 119, median: 88, min: 12, max: 1400
  - `decision_text`: The text used for determining the decision label
  - `decision_label`: **Primary suggested label**. Labels that can be used to train a model for judgment prediction:
    - `conflito-competencia`: Meta-decision. For example, a decision just to tell that Court A should rule this case and not Court B.
    - `no`: The appeal was denied
    - `not-cognized`: The appeal was not accepted to be judged by the court
    - `partial`: for partially favourable decisions
    - `prejudicada`: The case could not be judged for any impediment such as the appealer died or gave up on the case for instance.
    - `yes`: for full favourable decisions
  - `decision_unanimity_text`: Portuguese text to describe whether the decision was unanimous or not.
  - `decision_unanimity`: **Secondary suggested label**. Unified labels to describe whether the decision was unanimous or not; they can be used for model training as well  (Lage-Freitas et al., 2019).

### Data Splits

The data has been split randomly into 80% train (7686), 10% validation (961), 10% test (961).
Label Distribution
decision_label

decision_unanimity


## Dataset Creation

### Curation Rationale

This dataset was created to further the research on developing models for predicting Brazilian court decisions that are also able to predict whether the decision will be unanimous.

### Source Data

The data was scraped from *Tribunal de Justiça de Alagoas* (TJAL, the State Supreme Court of Alagoas (Brazil).

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
Lage-Freitas, A., Allende-Cid, H., Santana Jr, O., & Oliveira-Lage, L. (2019). Predicting Brazilian court decisions:
  - "In Brazil [...] lower court judges decisions might be appealed to Brazilian courts (*Tribiunais de Justiça*) to be reviewed by second instance court judges. In an appellate court, judges decide together upon a case and their decisions are compiled in Agreement reports named *Acóordãos*."

### Dataset Curators
André Lage Freitas, Joel Niklaus

### Licensing Information

[More Information Needed]

### Citation Information

[More Information Needed]

### Contributions

Thanks to [@kapllan](https://github.com/kapllan) and [@joelniklaus](https://github.com/joelniklaus) for adding this dataset.
