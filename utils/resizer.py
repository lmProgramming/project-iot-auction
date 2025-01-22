from PIL import Image
import os

image_directory = 'backend\images'

pixel_size = 100

resized_prefix = 'resized_'

for filename in os.listdir(image_directory):
    if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')) and not filename.startswith(resized_prefix):
        with Image.open(os.path.join(image_directory, filename)) as img:
            new_filename: str = f"{resized_prefix}{filename}"
            if os.path.exists(os.path.join(image_directory, new_filename)):
                os.remove(os.path.join(image_directory, new_filename))
            img = img.resize((pixel_size, pixel_size))

            img.save(os.path.join(image_directory, new_filename))

print("All images have been resized.")
