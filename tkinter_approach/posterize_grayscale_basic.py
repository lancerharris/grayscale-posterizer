from PIL import Image
import numpy as np

def posterize_grayscale_basic(input_path, output_path, levels):
    img = Image.open(input_path).convert("L")

    img_array = np.array(img)

    normalized_pixels = img_array / 255

    quantized_pixels = (normalized_pixels * (levels)).astype(int)

    result = (quantized_pixels / (levels) * 255).astype(np.uint8)

    return Image.fromarray(result)
