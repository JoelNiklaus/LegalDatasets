import datasets

from utils import save_and_compress

_LANGUAGES = [
    "bg",
    "cs",
    "da",
    "de",
    "el",
    "en",
    "es",
    "et",
    "fi",
    "fr",
    "ga",
    # "hr", # hr is not present in mc4
    "hu",
    "it",
    "lt",
    "lv",
    "mt",
    "nl",
    "pl",
    "pt",
    "ro",
    "sk",
    "sl",
    "sv",
]

for language in _LANGUAGES:
    print(language)
    dataset = datasets.load_dataset("csv", data_files=f"{language}/legal_mc4.csv")["train"]
    dataset = dataset.remove_columns("Unnamed: 0")

    save_and_compress(dataset, language, None)

for language in ["de", "en", "es"]:  # too large files
    print(language)
    dataset = datasets.load_dataset("json", data_files=f"{language}.jsonl")["train"]

    # KISS: just use train_test_split to divide
    split = dataset.train_test_split(test_size=0.5, shuffle=False)
    save_and_compress(split["train"], language, 0)
    save_and_compress(split["test"], language, 1)
