---
annotations_creators:
- expert-generated
- found
language_creators:
- found
language:
- de
license:
- cc-by-4.0
multilinguality:
- monolingual
pretty_name: Annotated German Legal Decision Corpus
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- multi-class-classification
---

# Dataset Card for Annotated German Legal Decision Corpus

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
- **Repository:** https://zenodo.org/record/3936490#.X1ed7ovgomK
- **Paper:** Urchs., S., Mitrović., J., & Granitzer., M. (2021). Design and Implementation of German Legal Decision
  Corpora. Proceedings of the 13th International Conference on Agents and Artificial Intelligence - Volume 2: ICAART,
  515–521. https://doi.org/10.5220/0010187305150521
- **Leaderboard:**
- **Point of Contact:** [Joel Niklaus](mailto:joel.niklaus.2@bfh.ch)

### Dataset Summary

This dataset consists of 200 randomly chosen judgments. In these judgments a legal expert annotated the components
conclusion, definition and subsumption of the German legal writing style Urteilsstil.

*"Overall 25,075 sentences are annotated. 5% (1,202) of these sentences are marked as conclusion, 21% (5,328) as
definition, 53% (13,322) are marked as subsumption and the remaining 21% (6,481) as other. The length of judgments in
sentences ranges from 38 to 862 sentences. The median of judgments have 97 sentences, the length of most judgments is on
the shorter side."* (Urchs. et al., 2021)

*"Judgments from 22 of the 131 courts are selected for the corpus. Most judgments originate from the VG Augsburg (59 /
30%) followed by the VG Ansbach (39 / 20%) and LSG Munich (33 / 17%)."* (Urchs. et al., 2021)

*"29% (58) of all selected judgments are issued in the year 2016, followed by 22% (44) from the year 2017 and 21% (41)
issued in the year 2015. [...] The percentages of selected judgments and decisions issued in 2018 and 2019 are roughly
the same. No judgments from 2020 are selected."* (Urchs. et al., 2021)

### Supported Tasks and Leaderboards

The dataset can be used for multi-class text classification tasks, more specifically, for argument mining.

### Languages

The language in the dataset is German as it is used in Bavarian courts in Germany.

## Dataset Structure

### Data Instances

Each sentence is saved as a json object on a line in one of the three files `train.jsonl`, `validation.jsonl`
or `test.jsonl`. The file `meta.jsonl` contains meta information for each court. The `file_number` is present in all
files for identification. Each sentence of the court decision was categorized according to its function.

### Data Fields

The file `meta.jsonl` contains for each row the following fields:

- `meta_title`: Title provided by the website, it is used for saving the decision
- `court`: Issuing court
- `decision_style`: Style of the decision; the corpus contains either *Urteil* (='judgment') or *Endurteil* (
  ='end-judgment')
- `date`: Date when the decision was issued by the court
- `file_number`: Identification number used for this decision by the court
- `title`: Title provided by the court
- `norm_chains`: Norms related to the decision
- `decision_guidelines`: Short summary of the decision
- `keywords`: Keywords associated with the decision
- `lower_court`: Court that decided on the decision before
- `additional_information`: Additional Information
- `decision_reference`: References to the location of the decision in beck-online
- `tenor`: Designation of the legal consequence ordered by the court (list of paragraphs)
- `legal_facts`: Facts that form the base for the decision (list of paragraphs)

The files `train.jsonl`, `validation.jsonl` and `test.jsonl` contain the following fields:

- `file_number`: Identification number for linkage with the file `meta.jsonl`
- `input_sentence`: The sentence to be classified
- `label`: In depth explanation of the court decision. Each sentence is assigned to one of the major components of
  German *Urteilsstil* (Urchs. et al., 2021) (list of paragraphs, each paragraph containing list of sentences, each
  sentence annotated with one of the following four labels):
  - `conclusion`: Overall result
  - `definition`: Abstract legal facts and consequences
  - `subsumption`: Determination sentence / Concrete facts
  - `other`: Anything else
- `context_before`: Context in the same paragraph before the input_sentence
- `context_after`: Context in the same paragraph after the input_sentence

### Data Splits

No split provided in the original release.

Splits created by Joel Niklaus. We randomly split the dataset into 80% (160 decisions, 19271 sentences) train, 10%
validation (20 decisions, 2726 sentences) and 10% test (20 decisions, 3078 sentences). We made sure, that a decision
only occurs in one split and is not dispersed over multiple splits.

Label Distribution

| label          |      train |   validation |      test |
|:---------------|-----------:|-------------:|----------:|
| conclusion     |        975 |          115 |       112 |
| definition     |       4105 |          614 |       609 |
| subsumption    |      10034 |         1486 |      1802 |
| other          |       4157 |          511 |       555 |
| total          |  **19271** |     **2726** |  **3078** |

## Dataset Creation

### Curation Rationale

Creating a publicly available German legal text corpus consisting of judgments that have been annotated by a legal
expert. The annotated components consist of *conclusion*, *definition* and *subsumption* of the German legal writing
style *Urteilsstil*.

### Source Data

#### Initial Data Collection and Normalization

*“The decision corpus is a collection of the decisions published on the website www.gesetze-bayern.de. At the time of
the crawling the website offered 32,748 decisions of 131 Bavarian courts, dating back to 2015. The decisions are
provided from the Bavarian state after the courts agreed to a publication. All decisions are processed by the publisher
C.H.BECK, commissioned by the Bavarian state. This processing includes anonymisation, key-wording, and adding of
editorial guidelines to the decisions.”* (Urchs. et al., 2021)

#### Who are the source language producers?

German courts from Bavaria

### Annotations

#### Annotation process

*“As stated above, the judgment corpus consist of 200 randomly chosen judgments that are annotated by a legal expert,
who holds a first legal state exam. Due to financial, staff and time reasons the presented iteration of the corpus was
only annotated by a single expert. In a future version several other experts will annotate the corpus and the
inter-annotator agreement will be calculated.”* (Urchs. et al., 2021)

#### Who are the annotators?

A legal expert, who holds a first legal state exam.

### Personal and Sensitive Information

*"All decisions are processed by the publisher C.H.BECK, commissioned by the Bavarian state. This processing includes **
anonymisation**, key-wording, and adding of editorial guidelines to the decisions.”* (Urchs. et al., 2021)

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

The SoMaJo Sentence Splitter has been used. Upon manual inspection of the dataset, we could see that the sentence
splitter had poor accuracy in some cases (see ```analyze_dataset()``` in ```convert_to_hf_dataset.py```). When creating
the splits, we thought about merging small sentences with their neighbors or removing them all together. However, since
we could not find an straightforward way to do this, we decided to leave the dataset content untouched.

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
Information*. Additional changes were made by Joel Niklaus ([Email](mailto:joel.niklaus.2@bfh.ch)
; [Github](https://github.com/joelniklaus)) and Veton Matoshi ([Email](mailto:veton.matoshi@bfh.ch)
; [Github](https://github.com/kapllan)).

### Licensing Information

[Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/legalcode)

### Citation Information

```
@dataset{urchs_stefanie_2020_3936490,
  author       = {Urchs, Stefanie and
                  Mitrović, Jelena},
  title        = {{German legal jugements annotated with judement 
                   style components}},
  month        = jul,
  year         = 2020,
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.3936490},
  url          = {https://doi.org/10.5281/zenodo.3936490}
}
```

```
@conference{icaart21,
  author = {Urchs., Stefanie and Mitrovi{\'{c}}., Jelena and Granitzer., Michael},
  booktitle = {Proceedings of the 13th International Conference on Agents and Artificial Intelligence - Volume 2: ICAART,},
  doi = {10.5220/0010187305150521},
  isbn = {978-989-758-484-8},
  issn = {2184-433X},
  organization = {INSTICC},
  pages = {515--521},
  publisher = {SciTePress},
  title = {{Design and Implementation of German Legal Decision Corpora}},
  year = {2021}
}
```

### Contributions

Thanks to [@kapllan](https://github.com/kapllan) and [@joelniklaus](https://github.com/joelniklaus) for adding this
dataset.
