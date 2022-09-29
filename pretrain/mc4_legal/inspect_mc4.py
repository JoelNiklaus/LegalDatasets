import pandas as pd

language = 'de'
df = pd.read_csv(f'{language}/legal_mc4.csv', nrows=5)

print(df.matches)
print(df.text)
