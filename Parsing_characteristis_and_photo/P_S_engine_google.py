# https://programmablesearchengine.google.com
import os
import requests
from PIL import Image
from io import BytesIO
from config import console_cloud_google_API_1, search_engine_id

# Ваши ключи и настройки
API_KEY = console_cloud_google_API_1
CX = search_engine_id
SEARCH_QUERY = "Belleza Denis Grande Shapetouch 60x120"  # Ваш поисковый запрос
SAVE_FOLDER = "downloaded_images"  # Папка для сохранения изображений

# Создание папки для изображений
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

# Функция для поиска изображений через Google Custom Search API
def search_images(query, api_key, cx, num=10):
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "cx": cx,
        "key": api_key,
        "searchType": "image",
        "num": num,  # Количество изображений (максимум 10 за запрос)
    }
    response = requests.get(url, params=params)
    data = response.json()
    if "items" in data:
        return [item["link"] for item in data["items"]]
    return []

# Функция для загрузки изображений
def download_image(url, save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки
        image = Image.open(BytesIO(response.content))
        image.save(save_path)
        print(f"Изображение сохранено: {save_path}")
    except Exception as e:
        print(f"Ошибка при загрузке {url}: {e}")

# Поиск и сохранение изображений
def main():
    print(f"Поиск изображений для: {SEARCH_QUERY}")
    image_urls = search_images(SEARCH_QUERY, API_KEY, CX, num=10)

    for idx, url in enumerate(image_urls):
        file_extension = url.split(".")[-1]
        file_name = os.path.join(SAVE_FOLDER, f"image_{idx + 1}.{file_extension}")
        download_image(url, file_name)

if __name__ == "__main__":
    main()
