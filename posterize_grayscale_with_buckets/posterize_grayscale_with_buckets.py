from PIL import Image
import numpy as np
import sys

def posterize_with_buckets(input_path, output_path, values, bin_levels=None):
    img = Image.open(input_path).convert("L")
    img_array = np.array(img)

    values = np.array(sorted(set(values)))
    num_buckets = len(values)

    if bin_levels:
        bin_levels = np.array(sorted(set(bin_levels)))
        if len(bin_levels) != num_buckets + 1:
            print("Number of bin levels must be equal to the number of values + 1")
            sys.exit(1)
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

    output_img = Image.fromarray(result)
    output_img.save(output_path)

    print(f"Posterized image saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python posterize_grayscale_with_buckets.py <input_path> <output_path> <values> [bin_markers]")
        print("Example values input: '10,80,150,200,255'")
        print("Optional bin levels input: '50,100,150,200'")
        sys.exit(1)

    input_image_path = sys.argv[1]
    output_image_path = sys.argv[2]

    try:
        values = list(map(int, sys.argv[3].split(",")))
    except ValueError:
        print("Values must be a list of integers between 0 and 255 separated by commas")
        sys.exit(1)

    bin_levels = None
    if len(sys.argv) == 5:
        try:
            bin_markers = list(map(int, sys.argv[4].split(",")))
            bin_levels = [0] + bin_markers + [255]
        except ValueError:
            print("Bin markers must be a comma-separated list of integers between 0 and 255 exclusive.")
            sys.exit(1)

    posterize_with_buckets(input_image_path, output_image_path, values, bin_levels)