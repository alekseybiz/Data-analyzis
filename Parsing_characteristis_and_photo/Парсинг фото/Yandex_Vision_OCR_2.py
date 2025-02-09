import cv2
import numpy as np
from PIL import Image
import base64
import json
import requests
from config import IAM_TOKEN

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
file_path = "ocean-ceramic-120x278-statuario-super-120x278-sm-plitka.a718eb1e9358.jpg"  # Укажите путь к вашему файлу

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

# Чтение изображения с использованием OpenCV
image = cv2.imread(file_path)

# Преобразуем изображение в серый цвет (для удобства пороговой обработки)
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Применяем пороговую обработку для выделения контрастных областей (контуры водяного знака)
_, threshold_image = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY)

# Находим контуры на изображении
contours, _ = cv2.findContours(threshold_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Рисуем контуры на исходном изображении (для отладки)
cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

# Сохраняем изображение с найденными контурами (для отладки)
# cv2.imwrite('contours_image.jpg', image)

# Открываем изображение для дальнейшей обработки
image_pil = Image.open(file_path)
image_height = image_pil.height  # Высота изображения

# Получаем координаты водяного знака из OCR
coordinates = get_watermark_coordinates(ocr_result, image_height, threshold=0.2)

if not coordinates:
    print("Водяной знак не найден в нижних 20% изображения.")
    exit()

# Прямоугольная область водяного знака
x_min = min(point["x"] for point in coordinates)
y_min = min(point["y"] for point in coordinates) - 5# немного увеличиваем область
x_max = max(point["x"] for point in coordinates) + 5
y_max = max(point["y"] for point in coordinates) + 9

# Замена области водяного знака с помощью инпейнтинга

# Преобразуем изображение в формат numpy
image_np = np.array(image_pil)

# Создаем маску для инпейнтинга, заполняя область водяного знака
mask = np.zeros((image_height, image_pil.width), dtype=np.uint8)
mask[y_min:y_max, x_min:x_max] = 255  # Маска для области водяного знака

# Применяем инпейтинг с использованием маски
restored_image = cv2.inpaint(image_np, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)

# Преобразуем изображение обратно в формат PIL для сохранения
restored_image_pil = Image.fromarray(restored_image)

# Сохраняем результат
output_path = "image_without_watermark_restored.jpg"
restored_image_pil.save(output_path)
print(f"Водяной знак удалён, изображение сохранено: {output_path}")
