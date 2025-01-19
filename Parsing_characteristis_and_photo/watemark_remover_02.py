from diffusers import StableDiffusionInpaintPipeline
import torch
from PIL import Image

# Загрузка модели
pipe = StableDiffusionInpaintPipeline.from_pretrained("runwayml/stable-diffusion-inpainting", torch_dtype=torch.float16)
pipe = pipe.to("cuda")

# Загрузка изображения
image = Image.open("new-trend-jast-60120jas11p-beige-polirovannyij-60x120-sm-plitka.5b2a4d059c77.jpg").convert("RGB")
mask = Image.open("w3dplitka_watermark_mask.png").convert("RGB")  # Белые области указывают на водяной знак

# Удаление водяного знака
result = pipe(prompt="Remove watermark", image=image, mask_image=mask).images[0]

# Сохранение результата
result.save("image_without_watermark.jpg")
