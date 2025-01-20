# Vision OCR
# Сервис распознавания текста на изображениях с помощью моделей машинного обучения
# Импортируем необходимые библиотеки

import base64
import json
import requests
from PIL import Image, ImageDraw
from config import IAM_TOKEN  # Импорт вашего IAM токена

# Идентификатор каталога
FOLDER_ID = "b1g56h2p36fq4g7gub7l"

# Функция для кодирования файла в Base64
def encode_file(file_path):
    with open(file_path, "rb") as fid:
        file_content = fid.read()
    return base64.b64encode(file_content).decode("utf-8")

# Функция для получения координат водяного знака
def get_watermark_coordinates(ocr_result, image_height, threshold=0.2):
    """
    Получить координаты водяного знака только в нижних threshold% изображения.
    """
    threshold_y = image_height * (1 - threshold)  # Вычисляем порог для нижних 20%
    for block in ocr_result["result"]["textAnnotation"]["blocks"]:
        for line in block["lines"]:
            if line["text"] == "3dplitka.ru":
                # Преобразуем координаты в целые числа
                coordinates = [
                    {"x": int(vertex["x"]), "y": int(vertex["y"])}
                    for vertex in line["boundingBox"]["vertices"]
                ]
                # Проверяем, все ли точки находятся в нижней части изображения
                if all(point["y"] >= threshold_y for point in coordinates):
                    return coordinates
    return None

# Путь к файлу изображения
file_path = "new-trend-jast-60120jas11p-beige-polirovannyij-60x120-sm-plitka.5b2a4d059c77.jpg"  # Укажите путь к вашему файлу

# Кодируем изображение в Base64
content_base64 = encode_file(file_path)

# Данные для запроса OCR API
data = {
    "mimeType": "image/jpeg",  # Указан корректный MIME-тип
    "languageCodes": ["*"],  # Распознавание на всех языках
    "content": content_base64  # Содержимое изображения в Base64
}

# URL для OCR API
url = "https://ocr.api.cloud.yandex.net/ocr/v1/recognizeText"

# Заголовки для запроса
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {IAM_TOKEN}",  # Токен авторизации
    "x-folder-id": FOLDER_ID,  # Идентификатор каталога
    "x-data-logging-enabled": "true"  # Логирование данных
}

# Выполняем POST-запрос
response = requests.post(url=url, headers=headers, data=json.dumps(data))

# Проверяем результат запроса
if response.status_code == 200:
    ocr_result = response.json()
    print("Распознанный текст:", ocr_result)
else:
    print("Ошибка:", response.status_code, response.text)
    exit()

# Открываем изображение
image = Image.open(file_path)
image_height = image.height  # Высота изображения

# Получаем координаты водяного знака
coordinates = get_watermark_coordinates(ocr_result, image_height, threshold=0.2)

if not coordinates:
    print("Водяной знак не найден в нижних 20% изображения.")
    exit()

# Прямоугольная область водяного знака
x_min = min(point["x"] for point in coordinates)
y_min = min(point["y"] for point in coordinates) - 5
x_max = max(point["x"] for point in coordinates) + 5
y_max = max(point["y"] for point in coordinates) + 9

# Удаляем водяной знак
try:
    # Замена области белым цветом
    draw = ImageDraw.Draw(image)
    draw.rectangle([x_min, y_min, x_max, y_max], fill="white")

    # Сохранение результата
    output_path = "image_without_watermark.jpg"
    image.save(output_path)
    print(f"Водяной знак удалён, изображение сохранено: {output_path}")

except Exception as e:
    print(f"Ошибка при удалении водяного знака: {e}")
