import pandas as pd

# data = [1, 2, 3, 4, 5]
# series = pd.Series(data)
# print(series)

data = {
    'Name' : ['Alice', 'Bob', 'Roma', 'Anna'],
    'Age' : [23, 45, 17, 20],
    'City' : ['New York', 'LA', 'Chicago', 'Moscow']
}

df = pd.DataFrame(data)
print(df)