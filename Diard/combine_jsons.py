import glob
import json
from pathlib import Path

import pandas as pd
import tqdm
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

folders = glob.glob('output/*')
dataset = []
skipped = 0

for folder in tqdm.tqdm(folders):
    folder = Path(folder)
    file_path = folder / 'jsons' / (folder.stem + ".json")
    try:
        json_content = json.loads(file_path.read_text())
    except FileNotFoundError:
        print(f"Could not find file at {file_path}. Continuing to the next file")
        skipped += 1
        continue
    text = ""
    for page in json_content:
        for section in page:
            text += section['content']

    try:
        language = detect(text)
    except LangDetectException:
        print(f"Could not detect language of file at {file_path}. Continuing to the next file")
        skipped += 1
        continue
    document = {"language": language, "type": "commentary", "title": folder.stem, "text": text}
    dataset.append(document)

print(f"Did not find files in {skipped} out of {len(folders)} files")

df = pd.DataFrame.from_records(dataset)
output_filename = "bger_commentaries.jsonl"
df.to_json(output_filename, orient="records")

print(f"Saved collected commentaries to {output_filename}")

