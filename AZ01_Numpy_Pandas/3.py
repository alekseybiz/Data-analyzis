import pandas as pd

df = pd.read_csv('hh.csv')

df['Test'] = [new for new in range(29)]

print(df)
