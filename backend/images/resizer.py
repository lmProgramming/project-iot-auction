from PIL import Image
import os

image_directory = r'backend\images'

pixel_size = 100

for filename in os.listdir(image_directory):
    if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        with Image.open(os.path.join(image_directory, filename)) as img:
            img = img.resize((pixel_size, pixel_size))

            img.save(os.path.join(image_directory, f"resized_{filename}"))

print("All images have been resized.")
