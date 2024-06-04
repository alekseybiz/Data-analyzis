import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

df = pd.read_csv('sources_prices.csv')
num_columns = len(df.columns)
print(f'Количество столбцов в файле CSV: {num_columns}')
num_rows = df.shape[0]
print(f'Число строк в DataFrame: {num_rows}')
browser = webdriver.Chrome()

for col in range(1, num_columns):
    print(col)
    tag = df.iloc[0, col]
    name = df.iloc[2, col]
    tag_name = tag + "." + name

    for row in range(3, num_rows):
        print(row)
        # row = 3
        item_name = df.iloc[row, 0]
        print(item_name)
        url = df.iloc[row, col]
        browser.get(url)
        # Явное ожидание появления элемента
        element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, tag_name)))
        price = element.text
        print(url)
        print(price)
        df.iloc[row, col] = price

# print(df)
df.to_csv('out_prices.csv', index=False)
browser.quit()








