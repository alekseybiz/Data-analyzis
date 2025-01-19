import cv2  # pip install opencv-python
import numpy as np

# Загрузка изображения
image = cv2.imread("image_with_watermark.jpg")

# Загрузка маски водяного знака (вы можете создать её вручную, исходя из текста)
# Черный цвет (0) для водяного знака, белый (255) для остальной области
watermark_mask = cv2.imread("watermark_mask.png", cv2.IMREAD_GRAYSCALE)

# Удаление водяного знака методом inpainting
result = cv2.inpaint(image, watermark_mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)

# Сохранение результата
cv2.imwrite("image_without_watermark.jpg", result)

# Отображение результата
cv2.imshow("Original Image", image)
cv2.imshow("Image without Watermark", result)
cv2.waitKey(0)
cv2.destroyAllWindows()