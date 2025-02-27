import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import posterize_grayscale_basic as pgb
import posterize_grayscale_with_buckets as pgwb

input_image = None
result_image = None
resized_result_image = None

preview_height = 300
preview_width = 300

def resize_image(image, max_size=(preview_width, preview_height)):
    image_copy = image.copy()
    image_copy.thumbnail(max_size, Image.Resampling.LANCZOS)
    return image_copy

def update_input_preview():
    global input_image
    input_path = input_entry.get()
    if input_path:
        try:
            image = Image.open(input_path)
            image = resize_image(image)
            input_image = ImageTk.PhotoImage(image)
            input_preview_label.config(image=input_image)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load input image:\n{str(e)}")

def update_result_preview(result_image):
    global resized_result_image
    try:
        # Resize preview result image to fit the preview area
        resized_result_image = resize_image(result_image)
        resized_result_image = ImageTk.PhotoImage(resized_result_image)
        result_preview_label.config(image=resized_result_image)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def select_input_file():
    path = filedialog.askopenfilename(
        title="Select Input Image",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp"), ("All Files", "*.*")]
    )
    if path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, path)
        update_input_preview()

def select_output_file():
    path = filedialog.asksaveasfilename(
        title="Select Output Image",
        defaultextension=".jpg",
        filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("BMP", "*.bmp"), ("All Files", "*.*")]
    )
    if path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, path)

def process_image():
    global result_image
    input_path = input_entry.get()
    output_path = output_entry.get()
    if not input_path:
        messagebox.showerror("Error", "Please select an input file.")
        return
    
    if mode.get() == "basic":
        try:
            levels = int(levels_entry.get())
            if levels < 2 or levels > 255:
                messagebox.showerror("Error", "Levels must be between 2 and 255.")
                return
            result_image = pgb.posterize_grayscale_basic(input_path, output_path, levels)
            update_result_preview(result_image)
        except ValueError:
            messagebox.showerror("Error", "Levels must be an integer.")
            return
    else:
        try:
            values = list(map(int, values_entry.get().split(",")))
        except ValueError:
            messagebox.showerror("Error", "Values must be comma-separated integers.")
            return
        bin_levels = None
        bin_str = bin_levels_entry.get().strip()
        if bin_str:
            try:
                bin_breakpoints = list(map(int, bin_str.split(",")))
                bin_levels = [0] + bin_breakpoints + [255]
                if len(bin_levels) != len(values) + 1:
                    messagebox.showerror("Error", "Number of bin breakpoints must be equal to the number of values - 1.")
                    return
            except ValueError:
                messagebox.showerror("Error", "Bin breakpoints must be comma-separated integers.")
                return
        try:
            result_image = pgwb.posterize_with_buckets(input_path, output_path, values, bin_levels)
            update_result_preview(result_image)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

def save_result_image():
    global result_image
    output_path = output_entry.get()
    if not result_image:
        messagebox.showerror("Error", "No result image to save.")
        return
    if not output_path:
        messagebox.showerror("Error", "Please select an output file.")
        return
    try:
        result_image.save(output_path)
        messagebox.showinfo("Success", f"Posterized image saved to:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not save result image:\n{str(e)}")

def on_enter_key(event):
    process_button.invoke()

def update_mode():
    """Switch between mode specifics dynamically without affecting layout."""
    if mode.get() == "basic":
        basic_frame.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        bucket_frame.grid_forget()
    else:
        bucket_frame.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        basic_frame.grid_forget()

root = tk.Tk()
root.title("Grayscale Posterizer")

root.bind("<Return>", on_enter_key)

mode = tk.StringVar(value="basic")

info_text = ('Welcome to Grayscale Posterizer!\nHere you can change a reference image to a grayscale image with a '
             'limited number of values. You can choose between two modes: "Basic" and "With Buckets".\n\n'
             'In "Basic" mode, you can specify the number of grayscale levels. In "With Buckets" mode, '
             'you can specify values and bin breakpoints to group grayscale levels into buckets.\n\n'
             'For the "With Buckets" mode, the values in the result will be the values you selected. The optional bin breakpoints '
             'will be used to group the original grayscale values into buckets between the breakpoints you select. Those pixels '
             'in those buckets will then be given the values you selected. The number of bin breakpoints must be equal to the '
                'number of values - 1.\n\n'
             'Select an input image, an output file, choose a mode, enter mode specifics, and click Process Image.')
info_message = tk.Message(root, text=info_text, width=2 * preview_width)
info_message.pack(padx=10, pady=10)

# Input File Frame
input_file_frame = tk.Frame(root)
input_file_frame.pack(fill=tk.X, padx=10, pady=5)
tk.Label(input_file_frame, text="Input File:").grid(row=0, column=0, sticky="e")
input_entry = tk.Entry(input_file_frame, width=50)
input_entry.grid(row=0, column=1, padx=5)
tk.Button(input_file_frame, text="Browse...", command=select_input_file).grid(row=0, column=2)

# Mode Selection Frame
mode_frame = tk.Frame(root)
mode_frame.pack(fill=tk.X, padx=10, pady=5)
tk.Label(mode_frame, text="Mode:").pack(side=tk.LEFT)
tk.Radiobutton(mode_frame, text="Basic", variable=mode, value="basic", command=update_mode).pack(side=tk.LEFT)
tk.Radiobutton(mode_frame, text="With Buckets", variable=mode, value="buckets", command=update_mode).pack(side=tk.LEFT)

# Mode Specifics Frame (Container)
mode_specifics_label_frame = tk.Frame(root)
mode_specifics_label_frame.pack(fill=tk.X, padx=10, pady=5)
tk.Label(mode_specifics_label_frame, text="Mode Specifics:").pack()

mode_specifics_frame = tk.Frame(root)
mode_specifics_frame.pack(fill=tk.X, padx=10, pady=5)

# Basic Mode Frame
basic_frame = tk.Frame(mode_specifics_frame)
basic_frame.grid(row=0, column=0, sticky="w", padx=10, pady=5)
tk.Label(basic_frame, text="Grayscale Levels (2-255):").grid(row=0, column=0, sticky="e")
levels_entry = tk.Entry(basic_frame)
levels_entry.grid(row=0, column=1, padx=5)
levels_entry.insert(0, "3")

# Bucket Mode Frame
bucket_frame = tk.Frame(mode_specifics_frame)
bucket_frame.grid(row=0, column=0, sticky="w", padx=10, pady=5)
bucket_frame.grid_forget()
tk.Label(bucket_frame, text="Values (comma separated list of values in 0-255 range):").grid(row=0, column=0, sticky="e")
values_entry = tk.Entry(bucket_frame)
values_entry.grid(row=0, column=1, padx=5)
values_entry.insert(0, "")

tk.Label(bucket_frame, text="Click on the gradient to add a grayscale value if you don't want to enter a number manually:").grid(row=1, column=0, columnspan=2, pady=(10, 0))
gradient_canvas = tk.Canvas(bucket_frame, width=256, height=30, bg='white')
gradient_canvas.grid(row=2, column=0, columnspan=2, pady=(0, 5))

def draw_gradient():
    gradient_canvas.delete("all")
    width = 256
    height = 30
    for x in range(width):
        gray = int((x / width) * 255)
        hex_color = f'#{gray:02x}{gray:02x}{gray:02x}'
        gradient_canvas.create_line(x, 0, x, height, fill=hex_color)

draw_gradient()

def on_gradient_click(event):
    canvas_width = gradient_canvas.winfo_width()
    # Convert the x-coordinate of the click to a grayscale value (0-255)
    gray_value = int((event.x / canvas_width) * 255)
    try:
        # Try to parse the current values from the entry
        current_values = values_entry.get().split(',')
        current_values = [int(v.strip()) for v in current_values if v.strip() != ""]
    except ValueError:
        current_values = []
    # Add the new grayscale value and sort
    current_values.append(gray_value)
    current_values = sorted(set(current_values))
    values_entry.delete(0, tk.END)
    values_entry.insert(0, ",".join(map(str, current_values)))

gradient_canvas.bind("<Button-1>", on_gradient_click)

tk.Label(bucket_frame, text="Optional Bin Breakpoints (comma separated list of breakpoints in 0-255 range):").grid(row=3, column=0, sticky="e")
bin_levels_entry = tk.Entry(bucket_frame)
bin_levels_entry.grid(row=4, column=1, padx=5)
bin_levels_entry.insert(0, "")

process_button = tk.Button(root, text="Process Image", command=process_image)
process_button.pack(pady=10)

preview_frame = tk.Frame(root)
preview_frame.pack(fill=tk.BOTH, padx=10, pady=10)

input_preview_container = tk.Frame(preview_frame, width=preview_width, height=preview_height, bd=2, relief="groove")
input_preview_container.pack(side=tk.LEFT, padx=5)
input_preview_container.pack_propagate(False)
tk.Label(input_preview_container, text="Input Preview").pack()
input_preview_label = tk.Label(input_preview_container)
input_preview_label.pack(expand=True)

result_preview_container = tk.Frame(preview_frame, width=preview_width, height=preview_height, bd=2, relief="groove")
result_preview_container.pack(side=tk.LEFT, padx=5)
result_preview_container.pack_propagate(False)
tk.Label(result_preview_container, text="Result Preview").pack()
result_preview_label = tk.Label(result_preview_container)
result_preview_label.pack(expand=True)

# Output File Frame
output_file_frame = tk.Frame(root)
output_file_frame.pack(fill=tk.X, padx=10, pady=5)
tk.Label(output_file_frame, text="Output File:").grid(row=1, column=0, sticky="e")
output_entry = tk.Entry(output_file_frame, width=50)
output_entry.grid(row=1, column=1, padx=5)
tk.Button(output_file_frame, text="Browse...", command=select_output_file).grid(row=1, column=2)

save_button = tk.Button(root, text="Save Result", command=save_result_image)
save_button.pack(pady=10)

root.mainloop()
