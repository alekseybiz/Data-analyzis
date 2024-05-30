import pandas as pd
from bs4 import BeautifulSoup
import requests


df = pd.read_csv('sources_prices.csv')
# print(df)

url = "https://www.plitkanadom.ru/collections/rossiiskaya-plitka/azori/eclipse/azori-eclipse-indigo-nastennaya-plitka-50-5x20-1"
response = requests.get(url)
   #print(response.text)
soup = BeautifulSoup(response.content, "html.parser")
price = soup.find('span', class_='new-price')
print(price.text)