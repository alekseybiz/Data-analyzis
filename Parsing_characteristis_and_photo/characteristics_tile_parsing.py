import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import openpyxl
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Настройте путь к вашему WebDriver
webdriver_path = r"C:\Users\Administrator\Documents\install\chromedriver\chromedriver.exe"  # Замените на путь к вашему драйверу

# Настройка сервиса для драйвера Chrome
service = Service(webdriver_path)

# Настройте путь к вашему файлу Excel
excel_path = "products.xlsx"

# Инициализация браузера
driver = webdriver.Chrome(service=service)

# Открываем таблицу Excel
workbook = openpyxl.load_workbook(excel_path)
sheet = workbook.active

# URL сайта для поиска
base_url = "https://3dplitka.ru/"  # Замените на URL вашего сайта

try:
    # Проходим по всем строкам таблицы
    for row in sheet.iter_rows(min_row=42, max_row=sheet.max_row):
        brand = row[4].value  # Значение из 5-го столбца ("Brand")
        collection = row[5].value  # Значение из 6-го столбца ("Collection")

        # Проверяем, что значения не пустые
        if not brand and not collection:
            continue

        brand_and_collection = brand + " " + collection
        print(f"Ищем: {brand_and_collection}")


        # Открываем сайт и выполняем поиск товара
        driver.get(base_url)
        search_box = driver.find_element(By.CLASS_NAME, "el-input__inner")  # Найдите селектор для поля поиска
        print(search_box.tag_name)  # Должно быть "input"
        search_box.send_keys(Keys.CONTROL + "a")  # Выделяем весь текст
        search_box.send_keys(Keys.DELETE)  # Удаляем выделенный текст
        search_box.send_keys(brand_and_collection)
        search_box.send_keys(Keys.RETURN)

        time.sleep(8)  # Ожидание загрузки результатов

        try:
            element = driver.find_element(By.XPATH, "//li[starts-with(@id, 'el-autocomplete-7611-item-')]")
            link = element.find_element(By.TAG_NAME, "a")
            href = link.get_attribute("href")
            print(f"Ссылка на товар: {href}")
            link.click()

            # Открываем первую ссылку на найденный товар
            # product_link = driver.find_element(By.CSS_SELECTOR, "a[data-v-f2647c94]")  # Замените на нужный селектор
            # print(f"product_link: {product_link}")
            # product_link.click()

            time.sleep(3)  # Ожидание загрузки страницы товара

            # Парсим характеристики товара
            for col_index, cell in enumerate(row[1:], start=2):
                characteristic_name = sheet.cell(row=1, column=col_index).value  # Название характеристики

                if not characteristic_name:
                    continue

                try:
                    # Найдите селектор для характеристики на странице товара
                    characteristic_value = driver.find_element(By.XPATH, f"//*[contains(text(), '{characteristic_name}')]/following-sibling::*").text
                    cell.value = characteristic_value
                except Exception as e:
                    print(f"Характеристика '{characteristic_name}' не найдена: {e}")

        except Exception as e:
            print(f"Товар '{product_name}' не найден: {e}")

finally:
    # Сохраняем изменения в Excel
    workbook.save(excel_path)
    print(f"Данные сохранены в {excel_path}")

    # Закрываем браузер
    driver.quit()
