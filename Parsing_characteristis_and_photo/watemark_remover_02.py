from diffusers import StableDiffusionInpaintPipeline
import torch
from PIL import Image

# Загружаем модель
# pipe = StableDiffusionInpaintPipeline.from_pretrained("runwayml/stable-diffusion-inpainting", torch_dtype=torch.float16)
# pipe = pipe.to("cuda")  # Используйте "cpu", если GPU недоступен

# Загрузка модели без float16
pipe = StableDiffusionInpaintPipeline.from_pretrained(
    "runwayml/stable-diffusion-inpainting"
)
pipe = pipe.to("cpu")

# Загрузка изображения и маски
image = Image.open("new-trend-jast-60120jas11p-beige-polirovannyij-60x120-sm-plitka.5b2a4d059c77.jpg").convert("RGB")
mask = Image.open("watermark_mask.jpg").convert("RGB")  # Белые области указывают на водяной знак

# Удаление водяного знака
result = pipe(prompt="Remove watermark", image=image, mask_image=mask).images[0]

# Сохранение результата
result.save("image_without_watermark.jpg")
