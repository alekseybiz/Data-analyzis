import  pandas as pd

data = {
    'Name': ['Alice', 'Bob', 'Richard'],
    'Age': [25, 30, 35],
    'City': ['New York', 'LA', 'Chicago']
}

df = pd.DataFrame(data)
print(df)
df.to_csv('out2.xls', index=False)