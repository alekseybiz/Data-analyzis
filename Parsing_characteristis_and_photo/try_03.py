import base64
import json
import requests
import numpy as np
import cv2
import torch
import torch.optim as optim
from PIL import Image
from deep_image_prior import net
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

# Чтение изображения с использованием OpenCV
image = cv2.imread(file_path)

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
y_min = min(point["y"] for point in coordinates) - 5  # немного увеличиваем область
x_max = max(point["x"] for point in coordinates) + 5
y_max = max(point["y"] for point in coordinates) + 9

# Замена области водяного знака с помощью инпейнтинга
image_np = np.array(image_pil)

# Создаем маску для инпейнтинга, заполняя область водяного знака
mask = np.zeros((image_height, image_pil.width), dtype=np.uint8)
mask[y_min:y_max, x_min:x_max] = 255  # Маска для области водяного знака

# Применяем инпейтинг с использованием маски
image_without_watermark = cv2.inpaint(image_np, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)

# Преобразуем изображение обратно в формат PIL для использования в DIP
image_without_watermark_pil = Image.fromarray(image_without_watermark)

# Преобразуем изображение в тензор PyTorch
image_tensor = torch.from_numpy(image_without_watermark).float().permute(2, 0, 1) / 255.0
image_tensor = image_tensor.unsqueeze(0)  # Добавляем размер батча

# Инициализация модели Deep Image Prior
model = net.DeepImagePrior()

# Определим функцию потерь (например, MSE)
criterion = torch.nn.MSELoss()

# Оптимизатор
optimizer = optim.Adam(model.parameters(), lr=0.1)

# Обучаем модель для восстановления изображения без водяного знака
for i in range(500):
    optimizer.zero_grad()
    output = model(image_tensor)
    loss = criterion(output, image_tensor)
    loss.backward()
    optimizer.step()

    if i % 50 == 0:
        print(f"Iteration {i}, Loss: {loss.item()}")

# Восстановленное изображение
restored_image = output.squeeze().permute(1, 2, 0).detach().numpy() * 255
restored_image = np.clip(restored_image, 0, 255).astype(np.uint8)

# Сохраняем восстановленное изображение
restored_image_pil = Image.fromarray(restored_image)
restored_image_pil.save("restored_image_without_watermark.jpg")
print("Водяной знак удалён, изображение восстановлено и сохранено.")
