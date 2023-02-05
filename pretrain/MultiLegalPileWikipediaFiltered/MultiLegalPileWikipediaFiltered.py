"""MultiLegalPileWikipediaFiltered"""

import json

import datasets
from huggingface_hub.file_download import hf_hub_url

try:
    import lzma as xz
except ImportError:
    import pylzma as xz

datasets.logging.set_verbosity_info()
logger = datasets.logging.get_logger(__name__)

_CITATION = """
"""

_DESCRIPTION = """
A filtered version of the MultiLegalPile dataset, together with wikipedia articles.
"""

_REPO_ID = "joelito/MultiLegalPileWikipediaFiltered"
_URL = f"https://huggingface.co/datasets/{_REPO_ID}"

_LANGUAGES = ["bg", "cs", "da", "de", "el", "en", "es", "et", "fi", "fr", "ga", "hr",
              "hu", "it", "lt", "lv", "mt", "nl", "pl", "pt", "ro", "sk", "sl", "sv"]

CASELAW = "caselaw"
CONTRACTS = "contracts"
LEGISLATION = "legislation"
OTHER = "other"
WIKIPEDIA = "wikipedia"
_TYPES = [CASELAW, CONTRACTS, LEGISLATION, OTHER, WIKIPEDIA]

_JURISDICTONS = ["Austria", "Belgium", "Bulgaria", "Croatia", "Czechia", "Denmark", "Estonia", "Finland",
                 "France", "Germany", "Greece", "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg",
                 "Malta", "Netherlands", "Poland", "Portugal", "Romania", "Slovakia", "Slovenia", "Spain", "Sweden",
                 "EU", "Switzerland", "UK", "US", "Canada", "N/A"]

# 1 is standard for most languages, types
NUMBER_OF_SHARDS = {lang: {type: 1 for type in _TYPES} for lang in _LANGUAGES}
for lang in _LANGUAGES:
    NUMBER_OF_SHARDS[lang][OTHER] = 0  # no other data for most languages
NUMBER_OF_SHARDS["en"][OTHER] = 15  # 15 other files for English

NUMBER_OF_SHARDS["cs"][CASELAW] = 2
NUMBER_OF_SHARDS["da"][LEGISLATION] = 2
NUMBER_OF_SHARDS["de"][CASELAW] = 5
NUMBER_OF_SHARDS["de"][LEGISLATION] = 2
NUMBER_OF_SHARDS["de"][WIKIPEDIA] = 5
NUMBER_OF_SHARDS["el"][LEGISLATION] = 2
NUMBER_OF_SHARDS["en"][CASELAW] = 66
NUMBER_OF_SHARDS["en"][CONTRACTS] = 16
NUMBER_OF_SHARDS["en"][LEGISLATION] = 5
NUMBER_OF_SHARDS["en"][WIKIPEDIA] = 11
NUMBER_OF_SHARDS["es"][WIKIPEDIA] = 3
NUMBER_OF_SHARDS["fr"][CASELAW] = 3
NUMBER_OF_SHARDS["fr"][LEGISLATION] = 2
NUMBER_OF_SHARDS["fr"][WIKIPEDIA] = 4
NUMBER_OF_SHARDS["ga"][CASELAW] = 0
NUMBER_OF_SHARDS["ga"][CONTRACTS] = 0
NUMBER_OF_SHARDS["it"][LEGISLATION] = 2
NUMBER_OF_SHARDS["it"][WIKIPEDIA] = 3
NUMBER_OF_SHARDS["nl"][LEGISLATION] = 2
NUMBER_OF_SHARDS["nl"][WIKIPEDIA] = 2
NUMBER_OF_SHARDS["pl"][WIKIPEDIA] = 2
NUMBER_OF_SHARDS["pt"][CASELAW] = 24
NUMBER_OF_SHARDS["pt"][WIKIPEDIA] = 2
NUMBER_OF_SHARDS["ro"][LEGISLATION] = 2


class MultiLegalPileWikipediaFilteredConfig(datasets.BuilderConfig):
    """BuilderConfig for MultiLegalPileWikipediaFiltered."""

    def __init__(self, name: str, **kwargs):
        """BuilderConfig for MultiLegalPileWikipediaFiltered.
        Args:
                name:           combination of language and type with _
                language:       One of bg,cs,da,de,el,en,es,et,fi,fr,ga,hr,hu,it,lt,lv,mt,nl,pl,pt,ro,sk,sl,sv or all
                type:           One of caselaw,contracts,legislation,other,wikipedia or all
              **kwargs: keyword arguments forwarded to super.
        """
        super(MultiLegalPileWikipediaFilteredConfig, self).__init__(**kwargs)
        self.name = name
        self.language = name.split("_")[0]
        self.type = name.split("_")[1]


class MultiLegalPileWikipediaFiltered(datasets.GeneratorBasedBuilder):
    """
    MultiLegalPileWikipediaFiltered:
    A filtered dataset of multilingual legal data and wikipedias in the EU languages
    """
    BUILDER_CONFIG_CLASS = MultiLegalPileWikipediaFilteredConfig

    BUILDER_CONFIGS = [MultiLegalPileWikipediaFilteredConfig(f"{language}_{type}")
                       for type in _TYPES + ["all"]
                       for language in _LANGUAGES + ["all"]]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "language": datasets.Value("string"),  # one of _LANGUAGES
                    "type": datasets.Value("string"),  # one of _TYPES
                    "jurisdiction": datasets.Value("string"),  # one of _JURISDICTONS
                    "text": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage=_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        def download_url(file_name):
            url = hf_hub_url(repo_id=_REPO_ID, filename=f"data/{file_name}.jsonl.xz", repo_type="dataset")
            return dl_manager.download(url)

        languages = _LANGUAGES if self.config.language == "all" else [self.config.language]
        types = _TYPES if self.config.type == "all" else [self.config.type]

        split_generators = []
        for split in [datasets.Split.TRAIN, datasets.Split.VALIDATION]:
            filepaths = []
            for language in languages:
                for type in types:
                    max_num_shards = NUMBER_OF_SHARDS[language][type] if split == datasets.Split.TRAIN else 1
                    for shard in range(max_num_shards):
                        try:
                            url = download_url(f"{language}_{type}_{split}.{shard}")
                            filepaths.append(url)
                        except Exception:
                            logger.exception(f"Error while processing url {url}")
            split_generators.append(
                datasets.SplitGenerator(name=split, gen_kwargs={"filepaths": filepaths})
            )
        return split_generators

    def _generate_examples(self, filepaths):
        """This function returns the examples in the raw (text) form by iterating on all the files."""
        id_ = 0
        for filepath in filepaths:
            logger.info(f"Generating examples from = {filepath}", )
            try:
                with xz.open(open(filepath, "rb"), "rt", encoding="utf-8") as f:
                    for line in f:
                        if line:
                            example = json.loads(line)
                            if example is not None and isinstance(example, dict):
                                yield id_, example
                                id_ += 1
            except Exception:
                logger.exception(f"Error while processing file {filepath}")
