from PIL import Image, ImageEnhance, ImageFilter
import numpy as np

# Load the image
img_path = 'office_3.jpg'
image = Image.open(img_path)

# Step 1: Enhance brightness and contrast
enhancer = ImageEnhance.Brightness(image)
image = enhancer.enhance(1.2) # Increase brightness
enhancer = ImageEnhance.Contrast(image)
image = enhancer.enhance(1.2) # Increase contrast

# Step 2: Enhance color
enhancer = ImageEnhance.Color(image)
image = enhancer.enhance(1.3) # Boost colors slightly

# Step 3: Slightly sharpen the image
image = image.filter(ImageFilter.SHARPEN)

# # Step 4: Simulate a clear sunny sky in the background
# # Convert image to array
# img_array = np.array(image)
#
# # Define color for "sunny sky" - a light blue
# sunny_sky_color = np.array([135, 206, 235])  # RGB for a clear light blue sky
#
# # Replace top part of the image which is usually the sky
# sky_area = img_array[0:100, :, :]  # Assuming the sky is in the top 100 pixels of the photo
# sky_area[:] = sunny_sky_color
#
# # Merge arrays back to form an image
# img_array[0:100, :, :] = sky_area
# image = Image.fromarray(img_array)

# Save the enhanced image
enhanced_img_path = 'enhanced_image.jpg'
image.save(enhanced_img_path)
