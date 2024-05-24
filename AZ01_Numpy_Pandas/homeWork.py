import pandas as pd

df = pd.read_csv('animal.csv')
# print(df)
df2 = pd.DataFrame(df)
print(df2.head(5))
print(df2.info())
print(df2.describe())

# print(df2)