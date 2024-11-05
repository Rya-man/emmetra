import tkinter as tk
from tkinter import filedialog, Label, Scale, Button, HORIZONTAL
from PIL import Image, ImageTk
import numpy as np
from processor.demosaic import demosaic_edge_based
from processor.denoise import denoise
from processor.gamma_correction import gamma_correction
from processor.sharpen import sharpen
from processor.white_balance import white_balance

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
        
        # Sliders for adjusting ISP parameters
        self.gamma_slider = Scale(root, from_=1.0, to=3.0, resolution=0.1, orient=HORIZONTAL, label="Gamma Correction")
        self.gamma_slider.pack(fill='x', padx=10, pady=5)
        
        self.sharpen_slider = Scale(root, from_=0, to=5, resolution=1, orient=HORIZONTAL, label="Sharpening Amount")
        self.sharpen_slider.pack(fill='x', padx=10, pady=5)

        # Process and Update Buttons
        process_button = Button(root, text="Process Image", command=self.update_image)
        process_button.pack(pady=10)

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
        
        # Apply ISP processing steps
        demosaiced_image = demosaic_edge_based(self.raw_image)
        white_balanced_image = white_balance(demosaiced_image)
        denoised_image = denoise(white_balanced_image)
        
        # Apply Gamma Correction and Sharpening based on slider values
        gamma_value = self.gamma_slider.get()
        gamma_corrected_image = gamma_correction(denoised_image, gamma_value)

        sharpen_amount = self.sharpen_slider.get()
        self.processed_image = sharpen(gamma_corrected_image, sharpen_amount)

        # Convert processed image to displayable format
        display_image = Image.fromarray((self.processed_image * 255).astype(np.uint8))  # Ensure 8-bit format
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

# Main application loop
root = tk.Tk()
app = ISPApp(root)
root.mainloop()
