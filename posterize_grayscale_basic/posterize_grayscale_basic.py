from PIL import Image
import numpy as np
import sys

def posterize_grayscale_basic(input_path, output_path, levels):
    img = Image.open(input_path).convert("L")

    img_array = np.array(img)

    normalized_pixels = img_array / 255

    quantized_pixels = (normalized_pixels * (levels - 1)).astype(int)

    result = (quantized_pixels / (levels - 1) * 255).astype(np.uint8)

    output_img = Image.fromarray(result)
    output_img.save(output_path)

    print(f"Posterized image saved to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python posterize_grayscale.py <input_path> <output_path> <levels>")
        sys.exit(1)

    input_image_path = sys.argv[1]
    output_image_path = sys.argv[2]
    levels = int(sys.argv[3])

    if levels < 2 or levels > 256:
        print("levels must be between 2 and 256")
        sys.exit(1)

    posterize_grayscale_basic(input_image_path, output_image_path, levels)