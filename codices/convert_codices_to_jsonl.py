from pathlib import Path

import pandas as pd
import json

obj = json.loads(Path("codices.json").read_text())[0]['Laws']
entries = []
for lang, lang_obj in obj.items():
    if lang == "ENG":
        lang = "en"
    if lang == "FRA":
        lang = "fr"
    for continent, continent_obj in lang_obj.items():
        print(continent)
        for country, text in continent_obj.items():
            entries.append({"lang": lang, "continent": continent, "country": country, "text": text})
df = pd.DataFrame(entries)
df.to_json("codices.jsonl", orient="records", lines=True)
