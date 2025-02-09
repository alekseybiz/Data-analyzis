from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time

# Настройте путь к вашему WebDriver
webdriver_path = r"C:\Users\Administrator\Documents\install\chromedriver\chromedriver.exe"



def search_images_yandex(query, max_results=10):
    """
    Выполняет поиск изображений в Яндекс Поиске с использованием Selenium.

    :param query: Поисковый запрос.
    :param max_results: Максимальное количество изображений для возврата.
    :return: Список URL найденных изображений.
    """
    # Настройка Selenium
    service = Service(webdriver_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Запуск в фоновом режиме
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Открытие Яндекс Поиска
        driver.get("https://yandex.com/images/")
        search_box = driver.find_element(By.NAME, "text")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        time.sleep(3)  # Ожидание загрузки страницы

        # Сбор изображений
        image_elements = driver.find_elements(By.CSS_SELECTOR, "img.serp-item__thumb")
        images = []

        for img in image_elements[:max_results]:
            img_url = img.get_attribute("src")
            if img_url and not img_url.startswith("data:image"):
                images.append("https:" + img_url)

        return images

    finally:
        driver.quit()


# Использование функции
query = "кошки"
results = search_images_yandex(query)

if results:
    print("Найденные изображения:")
    for idx, img_url in enumerate(results, start=1):
        print(f"{idx}: {img_url}")
else:
    print("Изображения не найдены.")
