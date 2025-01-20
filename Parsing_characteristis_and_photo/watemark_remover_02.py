import cv2
import pytesseract
from pytesseract import Output
import matplotlib.pyplot as plt


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Укажите путь к Tesseract OCR, если требуется
# pytesseract.pytesseract.tesseract_cmd = r'path_to_tesseract.exe'

# Загрузка изображения
image_path = "new-trend-jast-60120jas11p-beige-polirovannyij-60x120-sm-plitka.5b2a4d059c77.jpg"
image = cv2.imread(image_path)

# Преобразование в оттенки серого
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Увеличение контраста
gray = cv2.equalizeHist(gray)
# Удаление шума
gray = cv2.GaussianBlur(gray, (3,3), 0)
# Бинаризация
_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

custom_config = r'--oem 3 --psm 11'
d = pytesseract.image_to_data(gray, output_type=Output.DICT, config=custom_config)



# Добавляем флаг для отслеживания, был ли найден водяной знак
watermark_found = False

# Определение координат водяного знака
for i in range(len(d['text'])):
    if "plitka" in d['text'][i].lower():  # Ищем частичное совпадение
        print(f"Found text: {d['text'][i]}")
        x, y, w, h = d['left'][i], d['top'][i], d['width'][i], d['height'][i]
        print(f"Watermark found at: x={x}, y={y}, width={w}, height={h}")
        watermark_found = True

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
        print(f"файл сохранен: watermark_mask.jpg")
        break

# Добавьте отладочную печать всего найденного текста
print("Найденный текст:")
for text in d['text']:
    if text.strip():  # Печатаем только непустые строки
        print(text)

# Отображение изображения только если водяной знак найден
if watermark_found:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.show()
else:
    print("Водяной знак не найден")
