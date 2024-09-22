import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import openpyxl
import re

df = pd.read_excel('sources_xlsx.xlsx', engine='openpyxl')
num_columns = len(df.columns)
print(f'Количество столбцов в файле CSV: {num_columns}')
num_rows = df.shape[0]
print(f'Число строк в DataFrame: {num_rows}')

def extract_price(price_str):
    # Используем регулярное выражение для извлечения числовой части
    match = re.search(r'[\d\s]+', price_str)  # Ищем числа с пробелами
    if match:
        # Удаляем пробелы и преобразуем в float
        price_number = match.group(0).replace(' ', '')  # Убираем пробелы
        return float(price_number)  # Преобразуем в float
    return 0.0  # Если не нашли, возвращаем 0.0

chrome_options = Options()
chrome_options.add_argument("--verbose")

browser = webdriver.Chrome(options=chrome_options)

for row in range(1, num_rows): #for row in range(1, num_rows):
    print(f'Ряд: {row}')
    tag = df.iloc[row, 1]
    name = df.iloc[row, 2]
    tag_name = tag + "." + name
    print(f'Используемый тег: {tag_name}')

    for col in range(3, num_columns, 2):
        print(f'Ряд: {row}; Колонка: {col}')
        # item_name = df.iloc[0, col]
        # print(f'Товар: {item_name}')
        url = df.iloc[row, col]
        print(url)
        zakup = df.iloc[0, col]
        print(zakup)
        try:
            browser.get(url)
            # Явное ожидание появления элемента
            element = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, tag_name)))
            price = element.text
            print(f"Элемент найден, цена: {price}")
        except Exception as e:
            print(f"Произошла ошибка при поиске элемента: {type(e).__name__}: {e}")
            price = ""  # Присваиваем пустую строку вместо False

        print(f"Получена цена: {price}")
        # Проверяем, является ли price строкой
        if isinstance(price, str):
            extracted_price = extract_price(price)
            print(f"Извлеченная цена для ряда {row}, колонки {col}: {extracted_price}")
            df.iloc[row, col] = extracted_price
        else:
            df.iloc[row, col] = 0.0  # Или любое другое значение, если price не строка

        natsenka = (extracted_price / zakup - 1) * 100
        print(f"Наценка: {natsenka}")
        df.iloc[row, col+1] = natsenka

df = df.drop(df.columns[[1, 2]], axis=1)  # Удаляет колонки с индексами 1 и 2

try:
    df.to_excel('Prices_xlsx.xlsx', index=False, engine='openpyxl')
    print("Данные успешно сохранены в файл 'Prices_xls.xlsx'")
except:
    print("Ошибка записи в файл 'Prices_xlsx.xlsx' - не открыт ли файл?")


browser.quit()








