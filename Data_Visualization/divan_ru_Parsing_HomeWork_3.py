import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd
import matplotlib.pyplot as plt


driver = webdriver.Chrome()

# URL страницы
url = 'https://www.divan.ru/category/divany-i-kresla'
# Открытие страницы
driver.get(url)

#Ждем чтобы загрузилась страница
time.sleep(5)

#Парсинг цен
prices = driver.find_elements(By.XPATH, "//span[@class='ui-LD-ZU KIkOH']")
# print(prices)
for price in prices:
    price_text = price.get_attribute("innerText")  # Получаем текст из элемента
    print(price_text)
#
# Открытие CSV файла для записи
with open('prices.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Price'])  # Записываем заголовок столбца

    # Записываем цены в CSV файл
    for price in prices:
        writer.writerow([price.text])

# Закрытие драйвера
driver.quit()

def clean_price(price):
    # Удаляем "₽/мес." и преобразуем в число
    return int(price.replace('руб.', '').replace(' ', ''))


# Чтение данных из исходного CSV файла и их обработка
input_file = 'prices.csv'
output_file = 'cleaned_prices.csv'

with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Читаем заголовок и записываем его в новый файл
    header = next(reader)
    writer.writerow(header)

    # Обрабатываем и записываем данные строк
    for row in reader:
        clean_row = [clean_price(row[0])]
        writer.writerow(clean_row)

print(f"Обработанные данные сохранены в файл {output_file}")

# Открываем файл .csv для чтения
with open('cleaned_prices.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)

    total = 0
    count = 0
    data = []

    # Проходим по каждой строке файла
    for row in reader:
        for value in row:
            # Пытаемся преобразовать значение в число и добавляем его к общей сумме
            try:
                total += float(value)
                count += 1
                data.append(value)
                # print(f'data =  {data}')
            except ValueError:
                pass

# Вычисляем среднее значение
if count > 0:
    average = total / count
    print(f"Среднее значение: {average}")
else:
    print("Невозможно вычислить среднее значение, так как нет числовых данных в файле.")

# Гистограмма:
plt.hist(data, bins=5)

plt.xlabel("цена дивана")
plt.ylabel("кол-во диванов")
plt.title("Гистограмма: распределение цены диванов")

plt.show()
