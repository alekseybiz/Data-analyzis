import pandas as pd

df = pd.read_csv('hh.csv')

df['Test'] = [new for new in range(27)]

print(df)
# df.drop('Test', axis=1, inplace=True)
df.drop(26, axis=0, inplace=True)

print(df)

