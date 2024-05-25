import pandas as pd

# df = pd.read_csv('')
data = {
    'набор А': [85, 90, 95, 107, 105],
    'набор Б': [70, 80, 95, 110, 1200]
}
df = pd.DataFrame(data)

stdA = df['набор А'].std()
stdB = df['набор Б'].std()

print(f'стандартное отклонение 1-й набор - {stdA}')
print(f'стандартное отклонение 2-й набор - {stdB}')