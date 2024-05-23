import pandas as pd

df = pd.read_csv('World-happiness-report-2024.csv')
# print(df.tail(5))
# print(df.info())
# print(df.describe())
# print(df[['Country name', 'Regional indicator']])
# print(df[df['Healthy life expectancy'] > 0.7])
print(df.loc[73])