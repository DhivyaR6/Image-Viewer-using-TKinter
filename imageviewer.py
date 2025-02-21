import os
import glob
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer")
        self.root.geometry("800x600")

        self.image_list = []
        self.current_index = 0

        # UI Elements
        self.label = tk.Label(self.root, text="Select a folder to load images", font=("Arial", 14))
        self.label.pack(pady=20)

        self.canvas = tk.Canvas(self.root, width=600, height=400, bg="gray")
        self.canvas.pack()

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        self.prev_btn = tk.Button(btn_frame, text="<< Previous", command=self.prev_image, state=tk.DISABLED)
        self.prev_btn.grid(row=0, column=0, padx=10)

        self.select_btn = tk.Button(btn_frame, text="Select Folder", command=self.load_images)
        self.select_btn.grid(row=0, column=1, padx=10)

        self.next_btn = tk.Button(btn_frame, text="Next >>", command=self.next_image, state=tk.DISABLED)
        self.next_btn.grid(row=0, column=2, padx=10)

    def load_images(self):
        folder_path = filedialog.askdirectory()
        if not folder_path:
            return  # User canceled selection

        print(f"Selected folder: {folder_path}")  # Debugging

        # Get all image files (supports subfolders)
        self.image_list = glob.glob(os.path.join(folder_path, "**", "*.jpg"), recursive=True) + \
                          glob.glob(os.path.join(folder_path, "**", "*.jpeg"), recursive=True) + \
                          glob.glob(os.path.join(folder_path, "**", "*.png"), recursive=True) + \
                          glob.glob(os.path.join(folder_path, "**", "*.bmp"), recursive=True)

        print("Found images:", self.image_list)  # Debugging

        if not self.image_list:
            messagebox.showerror("Error", "No valid images found in the selected folder!")
            return

        self.current_index = 0
        self.display_image()

        # Enable navigation buttons
        self.prev_btn.config(state=tk.NORMAL)
        self.next_btn.config(state=tk.NORMAL)

    def display_image(self):
        if not self.image_list:
            return

        img_path = self.image_list[self.current_index]
        img = Image.open(img_path)
        img.thumbnail((600, 400))  # Resize while keeping aspect ratio

        self.img_tk = ImageTk.PhotoImage(img)
        self.canvas.create_image(300, 200, anchor=tk.CENTER, image=self.img_tk)
        self.label.config(text=f"Viewing {self.current_index + 1} of {len(self.image_list)}")

    def next_image(self):
        if self.current_index < len(self.image_list) - 1:
            self.current_index += 1
            self.display_image()

    def prev_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.display_image()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewer(root)
    root.mainloop()
