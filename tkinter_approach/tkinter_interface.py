import tkinter as tk
from tkinter import filedialog, messagebox

import posterize_grayscale_basic as pgb
import posterize_grayscale_with_buckets as pgwb

def select_input_file():
    path = filedialog.askopenfilename(
        title="Select Input Image",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp"), ("All Files", "*.*")]
    )
    if path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, path)

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
    input_path = input_entry.get()
    output_path = output_entry.get()
    if not input_path or not output_path:
        messagebox.showerror("Error", "Please select both input and output files.")
        return
    
    if mode.get() == "basic":
        try:
            levels = int(levels_entry.get())
            if levels < 2 or levels > 256:
                messagebox.showerror("Error", "Levels must be between 2 and 256.")
                return
            pgb.posterize_grayscale_basic(input_path, output_path, levels)
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
                    messagebox.showerror("Error", "Number of bin levels must be equal to the number of values - 1.")
                    return
            except ValueError:
                messagebox.showerror("Error", "Bin breakpoints must be comma-separated integers.")
                return
        try:
            pgwb.posterize_with_buckets(input_path, output_path, values, bin_levels)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
    messagebox.showinfo("Success", f"Posterized image saved to:\n{output_path}")

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
info_message = tk.Message(root, text=info_text, width=400)
info_message.pack(padx=10, pady=10)

# File Selection Frame
file_frame = tk.Frame(root)
file_frame.pack(fill=tk.X, padx=10, pady=5)
tk.Label(file_frame, text="Input File:").grid(row=0, column=0, sticky="e")
input_entry = tk.Entry(file_frame, width=50)
input_entry.grid(row=0, column=1, padx=5)
tk.Button(file_frame, text="Browse...", command=select_input_file).grid(row=0, column=2)

tk.Label(file_frame, text="Output File:").grid(row=1, column=0, sticky="e")
output_entry = tk.Entry(file_frame, width=50)
output_entry.grid(row=1, column=1, padx=5)
tk.Button(file_frame, text="Browse...", command=select_output_file).grid(row=1, column=2)

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
tk.Label(basic_frame, text="Grayscale Levels (2-256):").grid(row=0, column=0, sticky="e")
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

tk.Label(bucket_frame, text="Optional Bin Breakpoints (comma separated list of breakpoints in 0-255 range):").grid(row=1, column=0, sticky="e")
bin_levels_entry = tk.Entry(bucket_frame)
bin_levels_entry.grid(row=1, column=1, padx=5)
bin_levels_entry.insert(0, "")

# Process Button (Always at Bottom)
process_button = tk.Button(root, text="Process Image", command=process_image)
process_button.pack(pady=10)

root.mainloop()