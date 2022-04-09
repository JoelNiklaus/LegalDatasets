from pathlib import Path
import pandas as pd
import json
obj = json.loads(Path("description.json").read_text())[0]['Descriptions']
entries = []
for lang, lang_obj in obj.items():
    if lang == "ENG":
        lang = "en"
    if lang == "FRA":
        lang = "fr"
    try:
        for continent, continent_obj in lang_obj.items():
            print(continent)
            for country, text in continent_obj.items():
                entries.append({"lang": lang, "continent": continent, "country": country, "text": text})
    except:
        entries.append({"lang": lang, "continent": continent, "text": continent_obj})
df = pd.DataFrame(entries)
df.to_json("description.jsonl", orient="records", lines=True)