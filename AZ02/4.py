import pandas as pd
import matplotlib.pyplot as plt

data = {'value': [1, 2, 4, 7, 54, 7, 59, 289, -20]}
df = pd.DataFrame(data)

# df['value'].hist()

# df.boxplot(column='value')
# plt.show()

print(df.describe())

Q1 = df['value'].quantile(0.25)
Q3 = df['value'].quantile(0.75)
IQR = Q3 - Q1
downside = Q1 - 1.5 * IQR
upside = Q3 + 1.5 * IQR

df_new = df[(df['value'] >= downside) & (df['value'] <= upside)]
df_new.boxplot(column='value')
plt.show()
