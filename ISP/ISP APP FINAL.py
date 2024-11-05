import tkinter as tk
from tkinter import filedialog, Label, Scale, Button, HORIZONTAL, Checkbutton, BooleanVar
from PIL import Image, ImageTk
import numpy as np
from processor.demosaic import demosaic_edge_based
from processor.denoise import denoise
from processor.gamma_correction import gamma_correction
from processor.sharpen import sharpen
from processor.white_balance import white_balance  # Retain white balance import

class ISPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ISP App")
        
        # Initialize attributes
        self.raw_image = None
        self.processed_image = None
        
        # Load and Save Buttons
        load_button = Button(root, text="Load Image", command=self.load_image)
        load_button.pack(pady=5)

        save_button = Button(root, text="Save Image", command=self.save_image)
        save_button.pack(pady=5)

        # Checkboxes for optional processing steps
        self.apply_demosaic = BooleanVar(value=True)
        self.apply_denoise = BooleanVar(value=True)
        self.apply_gamma = BooleanVar(value=True)
        self.apply_sharpen = BooleanVar(value=True)

        Checkbutton(root, text="Demosaic", variable=self.apply_demosaic).pack()
        Checkbutton(root, text="Denoise", variable=self.apply_denoise).pack()
        Checkbutton(root, text="Gamma Correction", variable=self.apply_gamma).pack()
        Checkbutton(root, text="Sharpen", variable=self.apply_sharpen).pack()

        # Sliders for adjusting ISP parameters
        self.gamma_slider = Scale(root, from_=0.1, to=3.0, resolution=0.05, orient=HORIZONTAL, label="Gamma Correction")
        self.gamma_slider.pack(fill='x', padx=10, pady=5)
        self.gamma_slider.config(command=lambda val: self.update_image())

        self.sharpen_slider = Scale(root, from_=0, to=3.0, resolution=0.1, orient=HORIZONTAL, label="Sharpening Amount")
        self.sharpen_slider.pack(fill='x', padx=10, pady=5)
        self.sharpen_slider.config(command=lambda val: self.update_image())

        self.denoise_slider = Scale(root, from_=0, to=2.0, resolution=0.1, orient=HORIZONTAL, label="Denoising (Sigma)")
        self.denoise_slider.pack(fill='x', padx=10, pady=5)
        self.denoise_slider.config(command=lambda val: self.update_image())

        # Process and Update Buttons
        process_button = Button(root, text="Process Image", command=self.update_image)
        process_button.pack(pady=10)

        # Reset Parameters Button
        reset_button = Button(root, text="Reset Parameters", command=self.reset_parameters)
        reset_button.pack(pady=5)

        # Label to display images
        self.image_label = Label(root)
        self.image_label.pack()

    def load_image(self):
        # Load the RAW image file
        file_path = filedialog.askopenfilename()
        if file_path:
            self.raw_image = np.fromfile(file_path, dtype=np.uint16).reshape((1280, 1920))
            self.update_image()

    def update_image(self):
        if self.raw_image is None:
            return

        # Apply selected ISP processing steps
        image = self.raw_image
        
        if self.apply_demosaic.get():
            image = demosaic_edge_based(image)

        # Apply white balance automatically (without a UI control)
        image = white_balance(image)
        
        if self.apply_denoise.get():
            sigma = self.denoise_slider.get()
            image = denoise(image, sigma)
        if self.apply_gamma.get():
            gamma_value = self.gamma_slider.get()
            image = gamma_correction(image, gamma_value)
        if self.apply_sharpen.get():
            sharpen_amount = self.sharpen_slider.get()
            image = sharpen(image, sharpen_amount)

        self.processed_image = image

        # Convert processed image to displayable format
        display_image = Image.fromarray((self.processed_image * 255).astype(np.uint8))
        display_image = display_image.resize((640, 480))  # Resize for GUI display

        # Update image on GUI
        self.tk_image = ImageTk.PhotoImage(display_image)
        self.image_label.config(image=self.tk_image)

    def save_image(self):
        # Save the processed image
        if self.processed_image is not None:
            save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if save_path:
                Image.fromarray((self.processed_image * 255).astype(np.uint8)).save(save_path)

    def reset_parameters(self):
        # Reset sliders to default values
        self.gamma_slider.set(1.0)
        self.sharpen_slider.set(0)
        self.denoise_slider.set(0)
        self.update_image()

# Main application loop
root = tk.Tk()
app = ISPApp(root)
root.mainloop()
