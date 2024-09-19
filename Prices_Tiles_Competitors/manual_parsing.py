import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import openpyxl

chrome_options = Options()
chrome_options.add_argument("--verbose")  # Включение детализированных логов
service = Service(executable_path='chromedriver.exe', log_path='chromedriver.log')

browser = webdriver.Chrome(service=service, options=chrome_options)

## Если не получается парсинг, то пробуем вручную:
tag_name = "div.goods-card__price-text" # Введите через точку тег и атрибут тега
url = 'https://keram.ru/product/eclipse-indigo/' # Введите URL товара

browser.get(url)
print("Страница загружена")
# time.sleep(5)  # Задержка на 5 секунд

try:
    element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, tag_name)))
    print("Элемент найден")
    price = element.text
except Exception as e:
    print(f"Произошла ошибка поиске элемента: {type(e).__name__}: {e}")
    price = False

print(f"Получена цена: {price}")

browser.quit()