import pandas as pd
import matplotlib.pyplot as plt
data = {
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Al', 'Bobby', 'Charles', 'Davidson', 'Elis'],
    'mathematics': [4, 3, 5, 4, 3, 2, 5, 4, 4, 5],
    'english': [5, 2, 4, 4, 2, 3, 4, 5, 4, 5],
    'chemistry': [4, 3, 3, 4, 3, 4, 4, 5, 4, 5],
    'geography': [5, 4, 4, 5, 3, 3, 4, 4, 4, 5],
    'physics': [5, 3, 5, 5, 2, 3, 4, 5, 5, 5],
}

df = pd.DataFrame(data)
print(df)
print(f"Средняя оценка по предмету: {df['mathematics'].mean()}")
print(f"Средняя оценка по предмету: {df['english'].mean()}")
print(f"Средняя оценка по предмету: {df['chemistry'].mean()}")
print(f"Средняя оценка по предмету: {df['geography'].mean()}")
print(f"Средняя оценка по предмету: {df['physics'].mean()}")

print(f"Медианная оценка по предмету: {df['mathematics'].median()}")
print(f"Медианная оценка по предмету: {df['english'].median()}")
print(f"Медианная оценка по предмету: {df['chemistry'].median()}")
print(f"Медианная оценка по предмету: {df['geography'].median()}")
print(f"Медианная оценка по предмету: {df['physics'].median()}")

Q1_math = df['mathematics'].quantile(0.25)
Q3_math = df['mathematics'].quantile(0.75)
IQR = Q3_math - Q1_math

print(f"Q1 по математике: {Q1_math}")
print(f"Q3 по математике: {Q3_math}")
print(f"IQR по математике: {IQR}")
print(f"Cтандартное отклонение по математике: {df['mathematics'].std()}")