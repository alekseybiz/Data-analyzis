import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import requests

df = pd.read_csv('sources_prices.csv')
browser = webdriver.Chrome()

# №1
url = "https://www.plitkanadom.ru/collections/rossiiskaya-plitka/azori/eclipse/azori-eclipse-indigo-nastennaya-plitka-50-5x20-1"
browser.get(url)
# Явное ожидание появления элемента
element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.new-price')))
price = element.text
print(url)
print(price)
# browser.quit()

# №2
url = "https://santehnika-online.ru/product/plitka_nastennaya_azori_eclipse_indigo_glyantsevaya/351699/"
browser.get(url)
# Явное ожидание появления элемента
element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.b-price__price-core')))
price = element.text
print(url)
print(price)







