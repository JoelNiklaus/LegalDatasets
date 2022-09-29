# LegalDatasets

This repository serves as a collection of scrapers procuring and structuring various legal datasets

We want to link to already prepared legal datasets and prepare new datasets. These datasets can then be used for many
downstream tasks, such as pretraining language models or judgment prediction.

## Pretraining Datasets

Each of the pretraining datasets will be saved in jsonl format with the following fields:

- `id`: unique identifier for the document (uuid5 if not present yet)
- `type`: type of the document (e.g. `legislation`, `caselaw`, `commentary`)
- `language`: language of the document
- `jurisdiction`: jurisdiction of the document (e.g. `germany`)
- `title`: title of the document
- `date`: date of the document
- `url`: url of the document
- `metadata`: additional metadata of the document (as a json object)
- `text`: the text of the document

These pretraining datasets will be used to train the language models.

## Finetuning Datasets

We select a few (10 – 20) datasets to form a large-scale multi-lingual multi-jurisdictional benchmark (LEXTREME) for
finetuning.