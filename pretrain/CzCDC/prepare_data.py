import pandas as pd
import datasets
from utils import save_and_compress, select_and_clean

for court in ["ConCo", "SupAdmCo", "SupCo"]:
    df = pd.read_csv(f"{court}.csv", names=["file_name", "docket_number", "date", "court_abbreviation"],
                     encoding='latin-1')
    print(df)
    df["text"] = df.file_name.apply(lambda x: open(f"{court}/{x}", "r", encoding='latin-1').read().strip())
    print(df)
    df.drop(columns=["court_abbreviation"], inplace=True)

    df['type'] = 'caselaw'
    df['jurisdiction'] = 'Czechia'
    df['language'] = 'cs'

    df = select_and_clean(df)

    dataset = datasets.Dataset.from_pandas(df)

    if court == 'ConCo':
        court = "ConstitutionalCourt"
    elif court == 'SupAdmCo':
        court = "SupremeAdministrativeCourt"
    elif court == 'SupCo':
        court = "SupremeCourt"
    save_and_compress(dataset, court, None)
