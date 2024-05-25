import pandas as pd
import matplotlib.pyplot as plt
data = {
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Al', 'Bobby', 'Charles', 'Davidson', 'Elis'],
    'matemathics': ['4', '3', '5', '4', '3', '2', '5', '4', '4', '5'],
    'english': ['5', '2', '4', '4', '2', '3', '4', '5', '4', '5'],
    'chemistry': ['4', '3', '3', '4', '3', '4', '4', '5', '4', '5'],
    'geography': ['5', '4', '4', '5', '3', '3', '4', '4', '4', '5'],
    'physics': ['5', '3', '5', '5', '2', '3', '4', '5', '5', '5'],
}

df = pd.DataFrame(data)
print(df)