import pandas as pd

df = pd.read_csv('liustry.csv')

df['Test'] = [new for new in range(200)]

print(df)
