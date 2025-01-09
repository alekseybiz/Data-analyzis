# https://programmablesearchengine.google.com
import os
import requests
from PIL import Image
from io import BytesIO
import hashlib
from config import console_cloud_google_API_1, search_engine_id
import pytesseract

# Укажите путь к Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Путь к tesseract

API_KEY = console_cloud_google_API_1
CX = search_engine_id
product_name = "Belleza Denis Grande Shapetouch 60x120"
# product_name = "Belleza"

SAVE_FOLDER = "downloaded_images"
MIN_SIZE = 400
# MAX_RETRIES = 3

if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

image_hashes = set()
saved_images_count = 0

def search_images(query, api_key, cx, num=5):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "cx": cx,
        "key": api_key,
        "searchType": "image",
        "num": num,
        "imgSize": "large",
    }
    response = requests.get(url, params=params)
    print(f"HTTP Status Code: {response.status_code}")  # Проверка статуса ответа
    if response.status_code != 200:
        print(f"Ошибка API: {response.json()}")
        return []

    data = response.json()
    if "error" in data:
        print(f"Ошибка в данных: {data['error']}")
        return []
    query = query.lower().replace("x", " ").replace("х", " ").replace("kh", " ")

    query_words = set(query.split())  # Разбиваем запрос на слова и приводим их к нижнему регистру
    print(f"query_words {query_words}")

    filtered_images = []
    i = 0
    for item in data.get("items", []):
        i += 1
        title = item.get("title", "").lower()
        print(f"{i}. title {title}")
        link = item.get("link", "").lower()
        print(f"link: {link}")
        title_and_link = title + " " + link
        title_and_link = title_and_link.lower().replace("/", " ").replace("-", " ").replace(".", " ").replace("_", " ").replace(":", "")
        title_and_link = title_and_link.replace("x", " ").replace("х", " ").replace("kh", " ").replace("(", "").replace(")", "")

        print(f"title_and_link разбита: {title_and_link}")
        # Проверяем, содержатся ли все слова из query в title или link
        if query_words.issubset(set(title_and_link.split())):
            print(f"ключевые слова есть!")
            filtered_images.append(item)
        else:
            print(f"Нет ключевых слов в названии Title или Link: {item}")

    return filtered_images




def download_image(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))

        if image.width < MIN_SIZE and image.height < MIN_SIZE:
            print(f"Image too small:({image.width}x{image.height}) {url}")
            return None, None

        img_hash = hashlib.md5(response.content).hexdigest()
        if img_hash in image_hashes:
            print(f"Image already downloaded: {url}")
            return None, None

        image_hashes.add(img_hash)
        print(f"Downloaded successfully ({image.width}x{image.height}): {url}")
        return image, url

    except Exception as e:
        print(f"Download error {url}: {e}")
        return None, None


def contains_watermark(image):
    try:
        text = pytesseract.image_to_string(image)
        print(f"Извлеченный текст: {text}")
        watermark_keywords = ['.ru', '@', '.com']
        # return any(keyword in text.lower() for keyword in watermark_keywords)
        if any(keyword in text.lower() for keyword in watermark_keywords):
            print(f"Изображение содержит водяной знак")
            return True
    except Exception as e:
        print(f"Проверка на Watermark: {e}")
        return False


def save_image(image, save_path):
    try:
        image.save(save_path)
        global saved_images_count
        saved_images_count += 1
        print(f"Saved image {saved_images_count}: {save_path}")
        return True
    except Exception as e:
        print(f"Save error: {e}")
        return False


def main():
    # Поиск изображений плитки
    tile_query = f"{product_name}"
    print(f"tile_query: {tile_query}")
    search_results = search_images(tile_query, API_KEY, CX, num=10)
    print(f"Количество search_results: {len(search_results)}")
    if not search_results:
        print("Ничего не найдено.")
        return

    largest_image = None
    largest_area = 0

    for item in search_results:
        image_url = item['link']
        image, url = download_image(image_url)
        if image:
            print(f"Проверяем изображение, размер: {image.width}x{image.height}")

        # Проверяем изображение
        if image and not contains_watermark(image):
            image_area = image.width * image.height  # Вычисляем площадь изображения
            if image_area > largest_area:  # Если площадь больше текущего максимума
                largest_image = (image, url)
                largest_area = image_area
        else:
            print(f"Изображение отбраковано: {url}")

    # Сохраняем самое большое изображение
    if largest_image:
        image, url = largest_image
        filename = f"{product_name}.jpg"
        save_path = os.path.join(SAVE_FOLDER, filename)
        if save_image(image, save_path):
            print(f"Самое большое изображение {image.width}x{image.height} сохранено: {save_path}")
        else:
            print(f"Не удалось сохранить изображение: {url}")
    else:
        print("Подходящее изображение не найдено.")

if __name__ == "__main__":
    main()


