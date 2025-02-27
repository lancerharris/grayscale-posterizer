from PIL import Image
import numpy as np

def posterize_grayscale_basic(input_path, output_path, levels):
    img = Image.open(input_path).convert("L")

    img_array = np.array(img)

    normalized_pixels = img_array / 255

    quantized_pixels = (normalized_pixels * (levels)).astype(int)
    print("quantized_pixels made")

    result = (quantized_pixels / (levels) * 255).astype(np.uint8)

    output_img = Image.fromarray(result)
    output_img.save(output_path)

