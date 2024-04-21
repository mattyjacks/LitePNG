import tkinter as tk
from tkinter import filedialog, Entry, Label, Button
import imageio
import numpy as np
import os
from PIL import Image

class PNGCompressorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LitePNG - Resizer and Color Compressor")
        self.root.configure(bg='#ADD8E6')  # Light blue background
        self.file_list = []

        # Frame for Listbox and Scrollbar
        frame = tk.Frame(root, bg='#ADD8E6')
        frame.pack(pady=20)

        self.listbox = tk.Listbox(frame, width=150, height=10, justify=tk.RIGHT)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.config(yscrollcommand=scrollbar.set)

        # Buttons
        btn_frame = tk.Frame(root, bg='#ADD8E6')
        btn_frame.pack(fill=tk.X, padx=20, pady=10)

        btn_add = Button(btn_frame, text="Add PNG Files", command=self.add_files, padx=10, pady=5)
        btn_add.pack(side=tk.LEFT, fill=tk.X, expand=True)

        btn_remove = Button(btn_frame, text="Remove Selected", command=self.remove_selected, padx=10, pady=5)
        btn_remove.pack(side=tk.LEFT, fill=tk.X, expand=True)

        btn_compress = Button(btn_frame, text="Compress and Save", command=self.compress_and_save, padx=10, pady=5)
        btn_compress.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Resize scale and Quality settings
        settings_frame = tk.Frame(root, bg='#ADD8E6')
        settings_frame.pack(fill=tk.X, padx=20, pady=10)

        Label(settings_frame, text="Resize %:", bg='#ADD8E6').pack(side=tk.LEFT, padx=5)
        self.resize_entry = Entry(settings_frame, width=10)
        self.resize_entry.pack(side=tk.LEFT, padx=5)
        self.resize_entry.insert(0, "100")

        Label(settings_frame, text="Colors (0-256):", bg='#ADD8E6').pack(side=tk.LEFT, padx=5)
        self.colors_entry = Entry(settings_frame, width=10)
        self.colors_entry.pack(side=tk.LEFT, padx=5)
        self.colors_entry.insert(0, "256")

        Label(settings_frame, text="Presets:", bg='#ADD8E6').pack(side=tk.LEFT, padx=5)

        # Preset Buttons for Resize and Colors
        Button(settings_frame, text="Small", command=lambda: self.apply_preset(25, 16), padx=5, pady=5).pack(side=tk.LEFT, padx=5)
        Button(settings_frame, text="Full", command=lambda: self.apply_preset(100, 256), padx=5, pady=5).pack(side=tk.LEFT, padx=5)

    def apply_preset(self, resize_percentage, colors):
        self.resize_entry.delete(0, tk.END)
        self.resize_entry.insert(0, str(resize_percentage))
        self.colors_entry.delete(0, tk.END)
        self.colors_entry.insert(0, str(colors))

    def add_files(self):
        files = filedialog.askopenfilenames(filetypes=[("PNG files", "*.png")])
        for file in files:
            if file.endswith('.png') and file not in self.file_list:
                self.listbox.insert(tk.END, file)
                self.file_list.append(file)

    def remove_selected(self):
        selected_indices = self.listbox.curselection()
        for index in reversed(selected_indices):
            self.listbox.delete(index)
            del self.file_list[index]

    def compress_and_save(self):
        resize_percentage = float(self.resize_entry.get()) / 100
        colors = int(self.colors_entry.get())
        for file_path in self.file_list:
            image = imageio.imread(file_path)
            if resize_percentage != 1:
                new_dims = (int(image.shape[1] * resize_percentage), int(image.shape[0] * resize_percentage))
                image = np.array(Image.fromarray(image).resize(new_dims, Image.LANCZOS))
            if colors > 0 and colors <= 256:
                image = (image // (256 // colors)) * (256 // colors)
            save_path = filedialog.asksaveasfilename(initialfile=f"lite-{os.path.basename(file_path)}", defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if save_path:
                imageio.imwrite(save_path, image, format='PNG')
                print(f"Saved: {save_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PNGCompressorApp(root)
    root.mainloop()