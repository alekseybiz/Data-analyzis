import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

df = pd.read_csv('sources_prices.csv')

browser = webdriver.Chrome()

url = "https://www.plitkanadom.ru/collections/rossiiskaya-plitka/azori/eclipse/azori-eclipse-indigo-nastennaya-plitka-50-5x20-1"
browser.get(url)
# time.sleep(5)
# Явное ожидание появления элемента
element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.new-price')))

# element = browser.find_element_by_css_selector('span.new-price')

price = element.text
print(price)
browser.quit()





