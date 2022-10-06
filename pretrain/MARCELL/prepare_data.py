import pandas as pd
from pathlib import Path
from tqdm import tqdm

from utils import save_and_compress

languages = ["bg", "hu", "pl", "ro", "sk", "sl"]
jurisdictions = {"bg": "Bulgaria", "hu": "Hungary", "pl": "Poland", "ro": "Romania", "sk": "Slovakia", "sl": "Slovenia"}


def read_txt_files(path_to_file: str) -> dict:
    try:
        content = open(path_to_file, 'r').read()
        return {"text": content.strip()}
    except Exception as e:
        print('Error for this file: ', path_to_file)
        print(e)


for language in languages:
    print(language)
    path = Path(f'data/{language}/{language}-raw')  # Path to the downloaded folder

    files = [f for f in path.glob('**/*') if f.is_file()]
    files = [x for x in files if str(x).endswith('txt')]

    print('Number of documents to be processed: ', len(files))
    files_as_dict = [read_txt_files(x) for x in tqdm(files)]
    files_as_dict = [x for x in tqdm(files_as_dict) if x is not None]

    df = pd.DataFrame(files_as_dict)
    df['language'] = language
    df['jurisdiction'] = jurisdictions[language]
    df['type'] = 'legislation'
    df = df[['type', 'language', 'jurisdiction', 'text']]

    save_and_compress(df, f"data/{language}")
