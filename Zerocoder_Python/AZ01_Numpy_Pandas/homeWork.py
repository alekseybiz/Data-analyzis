import pandas as pd

df = pd.read_csv('animal.csv')
# print(df)
df2 = pd.DataFrame(df)
print(df2.head(15))
print(df2.info())
print(df2.describe())

value = df.iloc[0, 0]
print(value)

column_data = df['Животное']
print(column_data)

# print(df2)