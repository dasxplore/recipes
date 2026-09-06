import os
from PIL import Image, ImageOps
from pathlib import Path

base_path = Path(__file__).resolve().parent
print(f"base path: {base_path}")

def resize_and_compress_webp(input_path, output_path, max_width, max_height, quality=80):
    # 1. Open the source image
    with Image.open(input_path) as img:

        # 2. Resize using "contain" mode (preserves aspect ratio, fits inside bounding box)
        target_size = (max_width, max_height)
        resized_img = ImageOps.contain(img, target_size, method=Image.Resampling.LANCZOS)

        # 3. Save as WebP with explicit quality control
        resized_img.save(output_path, "WEBP", quality=quality)

valid_extensions = (".jpg", ".jpeg", ".png")

# Example usage:
for filename in os.listdir(base_path):
    if filename.lower().endswith(valid_extensions):
        file_name_without_ext = os.path.splitext(filename)[0]
        full_path_src = base_path / filename
        dest_path = base_path / f"{file_name_without_ext}.webp"

        resize_and_compress_webp(
            input_path=full_path_src,
            output_path=dest_path,
            max_width=1281, # 1280
            max_height=720,
            quality=80
        )
