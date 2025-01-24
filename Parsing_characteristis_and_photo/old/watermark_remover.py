import cv2
import numpy as np

# Загрузка изображения
image = cv2.imread("../new-trend-jast-60120jas11p-beige-polirovannyij-60x120-sm-plitka.5b2a4d059c77.jpg")

# Преобразование в градации серого
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Увеличение контраста с помощью equalizeHist
enhanced_image = cv2.equalizeHist(gray_image)

# Применение порогового значения для выделения водяного знака
_, watermark_mask = cv2.threshold(enhanced_image, 200, 255, cv2.THRESH_BINARY)

# Удаление мелкого шума с помощью морфологической обработки
kernel = np.ones((3, 3), np.uint8)
watermark_mask = cv2.morphologyEx(watermark_mask, cv2.MORPH_OPEN, kernel, iterations=2)
watermark_mask = cv2.morphologyEx(watermark_mask, cv2.MORPH_DILATE, kernel, iterations=1)

# Сохранение маски
cv2.imwrite("watermark_mask.jpg", watermark_mask)

# Отображение маски
cv2.imshow("Watermark Mask", watermark_mask)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Удаление водяного знака
result = cv2.inpaint(image, watermark_mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)

# Сохранение результата
cv2.imwrite("image_without_watermark.jpg", result)

# Отображение результата
cv2.imshow("Image without Watermark", result)
cv2.waitKey(0)
cv2.destroyAllWindows()
