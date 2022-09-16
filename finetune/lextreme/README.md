---
annotations_creators:
- other
language_creators:
- found
language:
- bg 
- cs 
- da 
- de 
- el 
- en
- es 
- et 
- fi 
- fr 
- ga
- hr 
- hu 
- it 
- lt 
- lv 
- mt
- nl 
- pl 
- pt 
- ro 
- sk 
- sl 
- sv
license:
- cc-by-4.0
multilinguality:
- multilingual
paperswithcode_id: null
pretty_name: "LEXTREME: A Multilingual Legal Benchmark for Natural Language Understanding"
size_categories:
- 1K<n<100K
source_datasets:
- original
task_categories:
- text-classification
- token-classification
task_ids:
- multi-class-classification
- multi-label-classification
- topic-classification
- text-classification-other-judgement-prediction
- named-entity-recognition
- named entity recognition and classification (NERC)

---

# Dataset Card for LEXTREME: A Multilingual Legal Benchmark for Natural Language Understanding

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
- **Repository:** 
- **Paper:** 
- **Leaderboard:**
- **Point of Contact:** [Joel Niklaus](joel.niklaus.2@bfh.ch)

### Dataset Summary

The dataset consists of 11 diverse multilingual legal NLU tasks. 6 tasks have one single configuration and 5 tasks have two or three configurations. This leads to a total of 18 tasks (8 single-label text classification tasks, 5 multi-label text classification tasks and 5 token-classification tasks).

### Supported Tasks and Leaderboards

The dataset supports the tasks of text classification and token classification.
In detail, we support the folliwing tasks and configurations:


| task                       |                 task type |                  configurations |                                                                                                   link |
|:---------------------------|--------------------------:|--------------------------------:|-------------------------------------------------------------------------------------------------------:|
| Brazilian Court Decisions  |       Judgment Prediction |           (judgment, unanimity) | [joelito/brazilian_court_decisions](https://huggingface.co/datasets/joelito/brazilian_court_decisions) |
| Swiss Judgment Prediction  |       Judgment Prediction |                         default |         [joelito/swiss_judgment_prediction](https://huggingface.co/datasets/swiss_judgment_prediction) |
| German Argument Mining     |           Argument Mining |                         default |       [joelito/german_argument_mining](https://huggingface.co/datasets/joelito/german_argument_mining) |
| Greek Legal Code           |      Topic Classification |      (volume, chapter, subject) |                                   [greek_legal_code](https://huggingface.co/datasets/greek_legal_code) |
| Online Terms of Service    | Unfairness Classification | (unfairness level, claus topic) |             [online_terms_of_service](https://huggingface.co/datasets/joelito/online_terms_of_service) |
| Covid 19 Emergency Event   |      Event Classification |                         default |             [covid19_emergency_event](https://huggingface.co/datasets/joelito/covid19_emergency_event) |
| MultiEURLEX                |      Topic Classification |     (level 1, level 2, level 3) |                                           [multi_eurlex](https://huggingface.co/datasets/multi_eurlex) |
| LeNER BR                   |  Named Entity Recognition |                         default |                                                   [lener_br](https://huggingface.co/datasets/lener_br) |
| LegalNERo                  |  Named Entity Recognition |                         default |                                         [legalnero](https://huggingface.co/datasets/joelito/legalnero) |
| Greek Legal NER            |  Named Entity Recognition |                         default |                             [greek_legal_ner](https://huggingface.co/datasets/joelito/greek_legal_ner) |
| MAPA                       |  Named Entity Recognition |                  (coarse, fine) |                                                   [mapa](https://huggingface.co/datasets/joelito/mapa) |


### Languages

The following languages are supported: bg , cs , da, de, el, en, es, et, fi, fr, ga, hr, hu, it, lt, lv, mt, nl, pl, pt, ro, sk, sl, sv

## Dataset Structure

### Data Instances

The file format is jsonl and three data splits are present for each configuration (train, validation and test). 

### Data Fields

[More Information Needed]

### Data Splits

[More Information Needed]

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

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

### Dataset Curators

[More Information Needed]

### Licensing Information

[More Information Needed]

### Citation Information

```
TODO add citation
```

### Contributions

Thanks to [@JoelNiklaus](https://github.com/joelniklaus) for adding this dataset.
