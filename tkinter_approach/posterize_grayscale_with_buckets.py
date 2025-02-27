from PIL import Image
import numpy as np

def posterize_with_buckets(input_path, output_path, values, bin_levels=None):
    img = Image.open(input_path).convert("L")
    img_array = np.array(img)

    values = np.array(sorted(set(values)))
    num_buckets = len(values)

    if bin_levels:
        bin_levels = np.array(sorted(set(bin_levels)))
        if len(bin_levels) != num_buckets + 1:
            raise ValueError("Number of bin levels must be equal to the number of values + 1")
        bucket_edges = bin_levels
    else:
        bucket_edges = np.linspace(0, 255, num_buckets + 1)

    def map_pixel(value):
        for i in range(num_buckets):
            if bucket_edges[i] <= value < bucket_edges[i + 1]:
                return values[i]
        return values[-1]
    
    vectorized_map = np.vectorize(map_pixel)
    result = vectorized_map(img_array).astype(np.uint8)

    return Image.fromarray(result)
