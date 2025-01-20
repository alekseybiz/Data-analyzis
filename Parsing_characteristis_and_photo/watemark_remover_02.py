import cv2
import pytesseract
from pytesseract import Output

# Укажите путь к Tesseract OCR, если требуется
# pytesseract.pytesseract.tesseract_cmd = r'path_to_tesseract.exe'

# Загрузка изображения
image_path = "vives-monocolor-octogono-negro-.f54e52ddaa08.jpg"
image = cv2.imread(image_path)

# Преобразование в оттенки серого
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Использование OCR для распознавания текста
d = pytesseract.image_to_data(gray, output_type=Output.DICT)

# Определение координат водяного знака
for i in range(len(d['text'])):
    if "3dplitka.ru" in d['text'][i]:  # Укажите текст водяного знака
        x, y, w, h = d['left'][i], d['top'][i], d['width'][i], d['height'][i]
        print(f"Watermark found at: x={x}, y={y}, width={w}, height={h}")

        # Создание маски водяного знака
        mask = cv2.rectangle(
            np.zeros_like(gray),
            (x, y),
            (x + w, y + h),
            (255, 255, 255),
            thickness=-1
        )

        # Сохранение маски
        cv2.imwrite("watermark_mask.jpg", mask)
        break
