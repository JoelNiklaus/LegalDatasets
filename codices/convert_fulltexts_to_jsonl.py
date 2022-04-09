from pathlib import Path

import pandas as pd
import json
import pycountry

lst = json.loads(Path("fulltext.json").read_text())['Full texts']
entries = []

for obj in lst:
    for continent, continent_lst in obj.items():
        continent = continent.split("/")[0].strip()
        print(continent)
        for continent_obj in continent_lst:
            for country, country_lst in continent_obj.items():
                country = country.split("/")[0].strip()
                print("\t", country)
                for country_obj in country_lst:
                    for lang, lang_lst in country_obj.items():
                        lang = lang.split("/")[0].strip()
                        # retrieve language code by name
                        try:
                            lang_code = pycountry.languages.get(name=lang).alpha_2
                        except AttributeError:
                            continue  # if we didn't find the language we don't save anything
                        print("\t\t", lang_code)
                        for text in lang_lst:
                            entry = {"lang": lang_code, "continent": continent, "country": country, "text": text}
                            entries.append(entry)

df = pd.DataFrame(entries)
df.to_json("fulltext.jsonl", orient="records", lines=True)
