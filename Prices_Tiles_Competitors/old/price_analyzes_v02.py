import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import openpyxl

df = pd.read_excel('sources_xlsx.xlsx', engine='openpyxl')
num_columns = len(df.columns)
print(f'Количество столбцов в файле CSV: {num_columns}')
num_rows = df.shape[0]
print(f'Число строк в DataFrame: {num_rows}')
# browser = webdriver.Chrome()

chrome_options = Options()
chrome_options.add_argument("--verbose")

browser = webdriver.Chrome(options=chrome_options)

for row in range(0, num_rows): #for row in range(0, num_rows):
    print(f'Ряд: {row}')
    tag = df.iloc[row, 1]
    name = df.iloc[row, 2]
    tag_name = tag + "." + name
    print(f'Используемый тег: {tag_name}')

    for col in range(3, num_columns):
        print(f'Ряд: {row}; Колонка: {col}')
        # item_name = df.iloc[0, col]
        # print(f'Товар: {item_name}')
        url = df.iloc[row, col]


        try:
            browser.get(url)
            # Явное ожидание появления элемента
            element = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, tag_name)))
            print("Элемент найден")
            price = element.text
        except Exception as e:
            print(f"Произошла ошибка при поиске элемента: {type(e).__name__}: {e}")
            price = False
        print(url)
        print(f"Получена цена: {price}")
        df.iloc[row, col] = price

df = df.drop(df.columns[[1, 2]], axis=1)  # Удаляет колонки с индексами 1 и 2

try:
    df.to_excel('Prices_xlsx.xlsx', index=False, engine='openpyxl')
    print("Данные успешно сохранены в файл 'Prices_xls.xlsx'")
except:
    print("Ошибка записи в файл 'Prices_xlsx.xlsx' - не открыт ли файл?")


browser.quit()








