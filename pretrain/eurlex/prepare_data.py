import os

import pandas as pd

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
    "hr",
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
_RESOURCE_TYPES = ["caselaw", "decision", "directive", "intagr", "proposal", "recommendation", "regulation"]


def prepare_data(language, resource_type, do_preproces=False):
    path = f"{language}/{resource_type}.jsonl"
    print(f"{language} {resource_type}")

    if do_preproces:
        print(f"Reading...")
        df = pd.read_json(path, lines=True)

        print("Preprocessing...")
        df.dropna(subset={"text"}, inplace=True)
        df.text = df.text.str.strip()  # remove beginning and trailing whitespace
        # df.date = pd.to_datetime(df.date, errors='coerce')
        print(df.head())

        print("Saving...")
        df.to_json(path, force_ascii=False, orient='records', lines=True)

    print("Compressing...")
    os.system(f'xz -zkf -T0 {path}')  # -TO to use multithreading

# Filter out rows without text
for language in _LANGUAGES:
    for resource_type in _RESOURCE_TYPES:
        prepare_data(language, resource_type)
