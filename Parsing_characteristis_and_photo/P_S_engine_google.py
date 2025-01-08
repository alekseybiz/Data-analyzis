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
BASE_QUERY = "Belleza Latin Travertine Crema Shapetouch 60x120"
SAVE_FOLDER = "downloaded_images"
MIN_SIZE = 600
MAX_RETRIES = 3

if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

image_hashes = set()
saved_images_count = 0


def search_images(query, api_key, cx, num=10):
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
    data = response.json()
    # print(f"Response from search: {data}")  # Для отладки
    return data.get("items", [])


def download_image(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))

        if image.width < MIN_SIZE and image.height < MIN_SIZE:
            print(f"Image too small: {url}")
            return None, None

        img_hash = hashlib.md5(response.content).hexdigest()
        if img_hash in image_hashes:
            print(f"Image already downloaded: {url}")
            return None, None

        image_hashes.add(img_hash)
        print(f"Downloaded successfully: {url}")
        return image, url

    except Exception as e:
        print(f"Download error {url}: {e}")
        return None, None


def contains_watermark(image):
    try:
        text = pytesseract.image_to_string(image)
        watermark_keywords = ['.ru', '@', '.com']
        return any(keyword in text.lower() for keyword in watermark_keywords)
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
    tile_query = f"{BASE_QUERY}"
    search_results = search_images(tile_query, API_KEY, CX, num=10)

    if not search_results:
        print("Ничего не найдено.")
        return

    for item in search_results:
        image_url = item['link']
        image, url = download_image(image_url)

        if image and not contains_watermark(image):
            filename = f"{BASE_QUERY}_{saved_images_count + 1}.jpg"
            save_path = os.path.join(SAVE_FOLDER, filename)
            save_image(image, save_path)

        if saved_images_count >= 5:  # Лимит сохраненных изображений
            print("Reached limit of saved images.")
            break


if __name__ == "__main__":
    main()

