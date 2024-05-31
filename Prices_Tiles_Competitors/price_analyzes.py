import pandas as pd
from bs4 import BeautifulSoup
import requests


df = pd.read_csv('sources_prices.csv')
# print(df)

url = "https://www.plitkanadom.ru/collections/rossiiskaya-plitka/azori/eclipse/azori-eclipse-indigo-nastennaya-plitka-50-5x20-1"
response = requests.get(url)
print(url)
print(response.ok)
soup = BeautifulSoup(response.content, "html.parser")
price = soup.find('span', class_='new-price')
print(price.text)

url = "https://leroymerlin.ru"
response = requests.get(url)
print(url)
print(response.status_code)
print(response.ok)
print(response.text)
   #print(response.text)
soup = BeautifulSoup(response.content, "html.parser")
# price_tag = soup.find('div', class_='p7uw7j7_pdp.primary-price.p1p5g0yu_pdp')
price_tag = soup.select_one('primary-price')
print(price_tag)
# price = price_tag.text.replace('\xa0', '')
# price = price_tag.get_text().replace('\xa0', '')
# print(price)

url = "https://santehnika-online.ru/product/plitka_nastennaya_azori_eclipse_indigo_glyantsevaya/351699/"
response = requests.get(url)
print(url)
print(response.status_code)
print(response.ok)
soup = BeautifulSoup(response.content, "html.parser")
price = soup.find('span', class_='b-price__price-core')
print(price)

# price = soup.find('div', class_='b-price__price.b-price__price--main')
# print(price.text)
