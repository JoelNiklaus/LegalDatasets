import pandas as pd

language = 'sk'
df = pd.read_csv(f'data/{language}/legal_mc4.csv', nrows=20)

print(df.to_string())
