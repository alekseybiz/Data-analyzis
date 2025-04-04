import os
import requests
import pandas as pd
from googleapiclient.discovery import build
from IPython.display import display, Image
import sys
from pathlib import Path
# # Определяем путь к корневой папке проекта (Data-analyzis)
# project_root = Path(__file__).resolve().parent.parent
# # Добавляем путь к корню проекта в sys.path
# sys.path.append(str(project_root / "AI_genegator"))
# # Теперь можно импортировать api_key из config
from config import console_cloud_google_API_1, search_engine_id


# Установите ваш API-ключ OpenAI
# openai.api_key = api_key

# excel_path = "for_parsing_try.xlsx"

developer_KEY = console_cloud_google_API_1
CX = search_engine_id

query = "New Trend Fenomen 60120FEM15P Light Полированный 60x120"
num_images = 7

service = build("customsearch", "v1", developerKey=developer_KEY)

def google_image_search(query, num_results):
    image_urls = []
    start_index = 1
    while len(image_urls) < num_results:
        num = min(10, num_results - len(image_urls))
        res = service.cse().list(
            q=query,
            cx=CX,
            searchType='image',
            num=num,
            start=start_index
        ).execute()

        for item in res.get('items', []):
            image_urls.append({
                'title': item.get('title'),
                'link': item.get('link'),
                'mime': item.get('mime'),
                'width': item.get('image', {}).get('width'),
                'height': item.get('image', {}).get('height')
            })
        start_index += num
    return image_urls

print("Ищем изображения...")
images = google_image_search(query, num_images)

df = pd.DataFrame(images)
display(df)

df.to_csv("images_info.csv", index=False, encoding='utf-8')
print("Информация об изображениях сохранена в images_info.csv")

images_dir = "../downloaded_images"
os.makedirs(images_dir, exist_ok=True)

def download_image(url, path):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(path, 'wb') as f:
            f.write(response.content)
        print(f"Скачано: {path}")
    except Exception as e:
        print(f"Ошибка при скачивании {url}: {e}")

print("Скачиваем изображения...")
for idx, row in df.iterrows():
    image_url = row['link']


    file_extension = os.path.splitext(image_url)[1]
    if not file_extension.lower() in [".jpg", ".jpeg", ".png", ".gif", ".bmp"]:
        file_extension = ".jpg"
    file_name = f"image_{idx+1}{file_extension}"
    file_path = os.path.join(images_dir, file_name)
    download_image(image_url, file_path)

print("Скачивание завершено.")


