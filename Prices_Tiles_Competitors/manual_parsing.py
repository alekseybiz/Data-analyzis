from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_argument("--verbose")

browser = webdriver.Chrome(options=chrome_options)

tag_name = "div.goods-card__price-text"
url = 'https://keram.ru/product/eclipse-indigo/'

browser.get(url)
print("Страница загружена")

try:
    # Увеличьте время ожидания или используйте visibility
    element = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, tag_name)))
    print("Элемент найден")
    price = element.text
except Exception as e:
    print(f"Произошла ошибка при поиске элемента: {type(e).__name__}: {e}")
    price = False

print(f"Получена цена: {price}")

browser.quit()