import pandas as pd

df = pd.read_csv('animal.csv')
print(df)

# df.fillna(0, inplace=True)
# df.dropna(inplace=True)
df.drop(7, axis=0, inplace=True)
print(df)
group = df.groupby('Пища')['Средняя продолжительность жизни'].mean()

print(group)

df.to_csv('output_animal.csv', index=False)