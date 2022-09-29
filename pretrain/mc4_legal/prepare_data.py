import os

import datasets

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

    path = f"{language}.jsonl"
    dataset.to_json(path, force_ascii=False)

    print("Compressing...")
    os.system(f'xz -zkf -T0 {path}')  # -TO to use multithreading
