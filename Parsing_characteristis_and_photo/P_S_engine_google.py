# https://programmablesearchengine.google.com
import os
import requests
from PIL import Image
from io import BytesIO
import hashlib
from config import console_cloud_google_API_1, search_engine_id
import pytesseract

# Ваши ключи и настройки
API_KEY = console_cloud_google_API_1
CX = search_engine_id
BASE_QUERY = "Belleza Latin Travertine Crema Shapetouch 60x120"  # Основной запрос
SAVE_FOLDER = "downloaded_images"  # Папка для сохранения изображений
MIN_SIZE = 600  # Минимальный размер хотя бы одной стороны изображения
MAX_RETRIES = 3  # Максимальное количество повторных попыток для интерьеров

# Создание папки для изображений
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

# Список хэшей для исключения повторяющихся изображений
image_hashes = set()

# Счётчик успешно сохранённых изображений
saved_images_count = 0


# Функция для поиска изображений через Google Custom Search API
def search_images(query, api_key, cx, num=10):
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "cx": cx,
        "key": api_key,
        "searchType": "image",
        "num": num,  # Количество изображений (максимум за запрос)
        "imgSize": "large",  # Только большие изображения
    }
    response = requests.get(url, params=params)
    data = response.json()
    if "items" in data:
        return [item["link"] for item in data["items"]]
    return []


# Функция для загрузки изображений
def download_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки
        image = Image.open(BytesIO(response.content))
        # Проверка минимального размера хотя бы одной стороны
        if image.width < MIN_SIZE and image.height < MIN_SIZE:
            print(f"Изображение {url} слишком маленькое ({image.width}x{image.height}). Пропускаем.")
            return None, None
        # Проверка на дубликаты (по хэш-сумме)
        img_hash = hashlib.md5(image.tobytes()).hexdigest()
        if img_hash in image_hashes:
            print(f"Изображение {url} уже загружено (дубликат). Пропускаем.")
            return None, None
        image_hashes.add(img_hash)
        print(f"Изображение хорошее ({image.width}x{image.height}): {url}")
        return image, url  # Возвращаем изображение и URL
    except Exception as e:
        print(f"Ошибка при загрузке {url}: {e}")
        return None, None


# Функция для проверки на водяные знаки
def contains_watermark(image):
    try:
        # Извлечение текста с помощью OCR
        text = pytesseract.image_to_string(image)
        # Проверяем, есть ли текст (водяные знаки часто содержат текст)
        return len(text.strip()) > 0
    except Exception as e:
        print(f"Ошибка проверки водяных знаков {image} : {e}")
        return False


# Сохранение изображения
def save_image(image, save_path):
    try:
        image.save(save_path)
        print(f"Изображение сохранено: {save_path}")
        return True
    except Exception as e:
        print(f"Ошибка сохранения изображения: {e}")
        return False


# Функция для поиска интерьеров
def find_and_save_interiors(query, min_required, retries=MAX_RETRIES):
    global saved_images_count  # Используем глобальную переменную
    saved_interiors = 0

    for attempt in range(retries):
        print(f"Попытка {attempt + 1}: поиск интерьеров для '{query}'")
        interior_image_urls = search_images(query, API_KEY, CX, num=20)  # Ищем больше, чтобы выбрать нужные

        for idx, url in enumerate(interior_image_urls):
            if saved_interiors >= min_required:
                break  # Останавливаемся, если сохранено достаточно интерьеров

            image, _ = download_image(url)
            if image and not contains_watermark(image):
                file_extension = url.split(".")[-1].split('?')[0]  # Убираем параметры из URL
                file_name = os.path.join(SAVE_FOLDER, f"{BASE_QUERY}_интерьер_{saved_images_count + 1}.{file_extension}")

                if save_image(image, file_name):
                    saved_images_count += 1
                    saved_interiors += 1
                    print(f"Изображение интерьера сохранено: {file_name}")

        if saved_interiors >= min_required:
            break  # Если удалось сохранить достаточно интерьеров, прекращаем дополнительные попытки

    return saved_interiors


# Поиск и сохранение изображений
def main():
    global saved_images_count  # Используем глобальную переменную

    # Шаг 1: Поиск изображений плитки
    print(f"Поиск изображений плитки для: {BASE_QUERY}")
    tile_query = f"{BASE_QUERY} плитка фото"
    tile_image_urls = search_images(tile_query, API_KEY, CX, num=5)

    # Скачиваем и выбираем самое большое изображение плитки
    largest_tile_image = None
    largest_tile_size = 0
    largest_tile_url = None

    for url in tile_image_urls:
        image, _ = download_image(url)
        if image and not contains_watermark(image):
            size = image.width * image.height
            if size > largest_tile_size:
                largest_tile_image = image
                largest_tile_size = size
                largest_tile_url = url

    if largest_tile_image:
        tile_save_path = os.path.join(SAVE_FOLDER, f"{BASE_QUERY}_плитка.jpg")
        if save_image(largest_tile_image, tile_save_path):
            saved_images_count += 1
            print(f"Самое большое изображение плитки сохранено: {tile_save_path}")

    # Шаг 2: Поиск интерьеров
    print(f"Поиск изображений интерьеров для: {BASE_QUERY}")
    interior_query = f"{BASE_QUERY} в интерьере"
    saved_interiors = find_and_save_interiors(interior_query, min_required=5)

    if saved_interiors < 5:
        print(f"Не удалось сохранить 5 интерьеров. Найдено и сохранено только: {saved_interiors}")

    print(f"Всего сохранено изображений: {saved_images_count}")


if __name__ == "__main__":
    main()

