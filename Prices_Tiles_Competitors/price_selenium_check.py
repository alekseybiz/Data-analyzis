import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

df = pd.read_csv('old/sources_prices.csv')
num_columns = len(df.columns)
print(f'Количество столбцов в файле CSV: {num_columns}')
num_rows = df.shape[0]
print(f'Число строк в DataFrame: {num_rows}')
browser = webdriver.Chrome()

col = 2
row = 4

tag = df.iloc[0, col]
name = df.iloc[2, col]
tag_name = tag + "." + name

url = df.iloc[row, col]
browser.get(url)
print(url)
# Явное ожидание появления элемента
element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, tag_name)))
price = element.text

print(price)

browser.quit()








