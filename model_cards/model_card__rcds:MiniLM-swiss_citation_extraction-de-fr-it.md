---
language:
  - multilingual
  - de
  - fr
  - it

tags:
  - multilingual

license: CC BY-SA

datasets:
  - rcds/swiss_citation_extraction
task: token-classification
---

# Model Card for rcds/MiniLM-swiss_citation_extraction-de-fr-it

This model is based on [microsoft/Multilingual-MiniLM-L12-H384](https://huggingface.co/microsoft/Multilingual-MiniLM-L12-H384) and has been fine-tuned on [rcds/swiss_citation_extraction](https://huggingface.co/datasets/rcds/swiss_citation_extraction).

## Model Details

### Model Description

- **Developed by:** Veton Matoshi: [huggingface](https://huggingface.co/kapllan); [email](mailto:msv3@bfh.ch)
- **Model type:** Transformer-based language model
- **Language(s) (NLP):** de, fr, it
- **License:** CC BY-SA

## Uses

### Direct Use and Downstream Use

You can utilize the raw model for token-classification tasks.

### Out-of-Scope Use

The model was fine-tuned to be used exclusively for token-classification.

## How to Get Started with the Model

See [huggingface tutorials](https://huggingface.co/docs/transformers/main_classes/pipelines).

## Training Details

This model was pretrained on [Multi Legal Pile](https://huggingface.co/datasets/joelito/Multi_Legal_Pile) ([Niklaus et al. 2023](https://arxiv.org/abs/2306.02069?utm_source=tldrai)).

Our pretraining procedure includes the following key steps:

(a) Warm-starting: We initialize our models from the original XLM-R checkpoints ([base](https://huggingface.co/xlm-roberta-base) and [large](https://huggingface.co/xlm-roberta-large)) of [Conneau et al. (2019)](https://proceedings.neurips.cc/paper/2019/file/c04c19c2c2474dbf5f7ac4372c5b9af1-Paper.pdf) to benefit from a well-trained base.

(b) Tokenization: We train a new tokenizer of 128K BPEs to cover legal language better. However, we reuse the original XLM-R embeddings for lexically overlapping tokens and use random embeddings for the rest.

(c) Pretraining: We continue pretraining on Multi Legal Pile with batches of 512 samples for an additional 1M/500K steps for the base/large model. We use warm-up steps, a linearly increasing learning rate, and cosine decay scheduling. During the warm-up phase, only the embeddings are updated, and a higher masking rate and percentage of predictions based on masked tokens are used compared to [Devlin et al. (2019)](https://aclanthology.org/N19-1423).

(d) Sentence Sampling: We employ a sentence sampler with exponential smoothing to handle disparate token proportions across cantons and languages, preserving per-canton and language capacity.

(e) Mixed Cased Models: Our models cover both upper- and lowercase letters, similar to recently developed large PLMs.

(f) Long Context Training: To account for long contexts in legal documents, we train the base-size multilingual model on long contexts with windowed attention. This variant, named Legal-Swiss-LF-base, uses a 15% masking probability, increased learning rate, and similar settings to small-context models.

### Training Data

This model was pretrained on [Multi Legal Pile](https://huggingface.co/datasets/joelito/Multi_Legal_Pile) ([Niklaus et al. 2023](https://arxiv.org/abs/2306.02069?utm_source=tldrai)).

#### Preprocessing

For further details see [Niklaus et al. 2023](https://arxiv.org/abs/2306.02069?utm_source=tldrai)

#### Training Hyperparameters

- batche size: 512 samples
- Number of steps: 1M/500K for the base/large model
- Warm-up steps for the first 5\% of the total training steps
- Learning rate: (linearly increasing up to) $1e\!-\!4$
- Word masking: increased 20/30\% masking rate for base/large models respectively

## Evaluation

For further insights into the evaluation, we refer to the [trainer state](https://huggingface.co/joelito/legal-xlm-roberta-large/blob/main/last-checkpoint/trainer_state.json). Additional information is available in the [tensorboard](https://huggingface.co/joelito/legal-xlm-roberta-large/tensorboard).

For performance on downstream tasks, such as [LEXTREME](https://huggingface.co/datasets/joelito/lextreme) ([Niklaus et al. 2023](https://arxiv.org/abs/2301.13126)) or [LEXGLUE](https://huggingface.co/datasets/lex_glue) ([Chalkidis et al. 2021](https://arxiv.org/abs/2110.00976)), we refer to the results presented in Niklaus et al. (2023) [1](https://arxiv.org/abs/2306.02069), [2](https://arxiv.org/abs/2306.09237).

### Model Architecture and Objective

It is a RoBERTa-based model. Run the following code to view the architecture:

```
from transformers import AutoModel
model = AutoModel.from_pretrained('model_identifier')
print(model)

RobertaModel(
  (embeddings): RobertaEmbeddings(
    (word_embeddings): Embedding(128000, 1024, padding_idx=0)
    (position_embeddings): Embedding(514, 1024, padding_idx=0)
    (token_type_embeddings): Embedding(1, 1024)
    (LayerNorm): LayerNorm((1024,), eps=1e-05, elementwise_affine=True)
    (dropout): Dropout(p=0.1, inplace=False)
  )
  (encoder): RobertaEncoder(
    (layer): ModuleList(
      (0-23): 24 x RobertaLayer(
        (attention): RobertaAttention(
          (self): RobertaSelfAttention(
            (query): Linear(in_features=1024, out_features=1024, bias=True)
            (key): Linear(in_features=1024, out_features=1024, bias=True)
            (value): Linear(in_features=1024, out_features=1024, bias=True)
            (dropout): Dropout(p=0.1, inplace=False)
          )
          (output): RobertaSelfOutput(
            (dense): Linear(in_features=1024, out_features=1024, bias=True)
            (LayerNorm): LayerNorm((1024,), eps=1e-05, elementwise_affine=True)
            (dropout): Dropout(p=0.1, inplace=False)
          )
        )
        (intermediate): RobertaIntermediate(
          (dense): Linear(in_features=1024, out_features=4096, bias=True)
          (intermediate_act_fn): GELUActivation()
        )
        (output): RobertaOutput(
          (dense): Linear(in_features=4096, out_features=1024, bias=True)
          (LayerNorm): LayerNorm((1024,), eps=1e-05, elementwise_affine=True)
          (dropout): Dropout(p=0.1, inplace=False)
        )
      )
    )
  )
  (pooler): RobertaPooler(
    (dense): Linear(in_features=1024, out_features=1024, bias=True)
    (activation): Tanh()
  )
)

```

### Compute Infrastructure

Google TPU.

#### Hardware

Google TPU v3-8

#### Software

pytorch, transformers.

## Citation [optional]

```

@article{Niklaus2023MultiLegalPileA6,
  title={MultiLegalPile: A 689GB Multilingual Legal Corpus},
  author={Joel Niklaus and Veton Matoshi and Matthias Sturmer and Ilias Chalkidis and Daniel E. Ho},
  journal={ArXiv},
  year={2023},
  volume={abs/2306.02069}
}

```

## Model Card Authors

Joel Niklaus: [huggingface](https://huggingface.co/joelito); [email](mailto:joel.niklaus.2@bfh.ch)

Veton Matoshi: [huggingface](https://huggingface.co/kapllan); [email](mailto:msv3@bfh.ch)

## Model Card Contact

Joel Niklaus: [huggingface](https://huggingface.co/joelito); [email](mailto:joel.niklaus.2@bfh.ch)

Veton Matoshi: [huggingface](https://huggingface.co/kapllan); [email](mailto:msv3@bfh.ch)
