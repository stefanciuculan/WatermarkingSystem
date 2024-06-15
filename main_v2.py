from tkinter import *
from tkinter import filedialog, font, PhotoImage
from PIL import Image, ImageDraw, ImageFont, ImageTk
import cv2 
import numpy as np

class Watermarking:
    def __init__(self):
        self.image = None
        self.image_label = None
        self.copy_of_image = None
        
        # Configure window aspect
        self.window = Tk()
        self.window.config(bg="#404040")
        self.window.title("ThirstyMark")
        
        # Get screen width and height
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # Set window size to the screen size
        self.window.geometry(f"{screen_width}x{screen_height}")
        
        # Create a menu on the right side of the screen
        menu = Frame(self.window, width=300, height=screen_height, bg="#454545")
        menu.pack(side="right", fill="y", expand=False)
        
        # Create a canvas to display the image
        self.canvas = Canvas(self.window, width=1000, height=700, bg="#45474B")
        self.canvas.pack(side="left", padx=50, pady=10, fill="y")
        
        # Create button for opening the image
        open_image_button = Button(menu, text="Open Image", fg="#FFF", bg="#45474B", width=29, height=2, command=self.open_image)
        open_image_button.pack(side="top", padx=5, pady=40)
        
        # Create an entry widget
        text_font = font.Font(size=14)
        self.text_area = Text(menu, width=21, height=3, font=text_font)
        self.text_area.pack(side="top", padx=5)
        
        # Create button for adding text as watermark
        add_text_button = Button(menu, text="Add Text", fg="#FFF", bg="#45474B", width=29, height=2, command=self.add_text)
        add_text_button.pack(side="top", padx=5, pady=10)
        
        # Create button for selecting the logo
        select_logo_button = Button(menu, text="Select Logo", fg="#FFF", bg="#45474B", width=29, height=2, command=self.add_logo)
        select_logo_button.pack(side="top", padx=5, pady=10)
        
        # Create button for saving the image
        save_button = Button(menu, text="Save", fg="#FFF", bg="#45474B", width=29, height=2, command=self.save_image)
        save_button.pack(side="top", padx=5, pady=10)
        
        # Create button for detecting the watermark 
        detect_button = Button(menu, text="Detect Watermark", fg="#FFF", bg="#45474B", width=29, height=2, command=self.detect_watermark)
        detect_button.pack(side="top", padx=5, pady=10)

        
        self.window.mainloop()
    
    def open_image(self):
        image_path = filedialog.askopenfilename()
        self.image = Image.open(image_path)
        self.copy_of_image = self.image
        
        # Resize the image to fit within the canvas dimensions
        width, height = self.image.size
        max_width = self.canvas.winfo_reqwidth()
        max_height = self.canvas.winfo_reqheight()
        
        if width > max_width or height > max_height:
            ratio = min(max_width / width, max_height / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            self.copy_of_image = self.copy_of_image.resize((new_width, new_height), Image.LANCZOS)
        
        # Display the copy of the image on the canvas
        self.photo_image = ImageTk.PhotoImage(self.copy_of_image)
        self.canvas.create_image((max_width - new_width) // 2, (max_height - new_height) // 2, image=self.photo_image, anchor=NW)
        
    def add_text(self):
        width, height = self.image.size
        resized_width, resized_height = self.copy_of_image.size
        
        # Create a new image with transparent background for both the resized preview image and the initial image 
        watermark = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        resized_watermark = Image.new('RGBA', (resized_width, resized_height), (0, 0, 0, 0))
        
        # Draw diagonal lines on the background
        draw = ImageDraw.Draw(watermark)
        resized_draw = ImageDraw.Draw(resized_watermark)
        
        for i in range(0, width + height, 50):
            draw.line([(0, height - i), (i, height)], fill=(255, 255, 255, 20), width=5)
            
        for i in range(0, resized_width + resized_height, 50):
            resized_draw.line([(0, resized_height - i), (i, resized_height)], fill=(255, 255, 255, 20), width=5)
        
        # Get text from text area
        text = self.text_area.get("1.0", "end-1c")
        
        # Choose font and calculate text dimensions
        font_size = int(width // 35)
        font = ImageFont.truetype("arial.ttf", font_size)
        
        text_width = draw.textlength(text, font)
        text_height = font_size
        
        # Choose font and calculate text dimensions for the preview image
        resized_font_size = int(resized_width // 35)
        resized_font = ImageFont.truetype("arial.ttf", resized_font_size)
        
        resized_text_width = resized_draw.textlength(text, resized_font)
        resized_text_height = resized_font_size
        
        # Calculate text position
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        resized_x = (resized_width - resized_text_width) // 2
        resized_y = (resized_height - resized_text_height) // 2
        
        # Draw text on the watermark
        draw.text((x, y), text, font=font, fill=(255, 255, 255, 100), stroke_width=3, stroke_fill=(0, 0, 0, 100))
        
        resized_draw.text((resized_x, resized_y), text, font=resized_font, fill=(255, 255, 255, 100), stroke_width=3, stroke_fill=(0, 0, 0, 100))
        
        # Composite watermark with text onto the original image, also on the image used for the preview
        self.image.paste(watermark, (0, 0), watermark)
        
        self.copy_of_image.paste(resized_watermark, (0, 0), resized_watermark)
        
        # Update the canvas with the new image
        self.photo_image = ImageTk.PhotoImage(self.copy_of_image)
        self.canvas.create_image(((self.canvas.winfo_reqwidth() - self.copy_of_image.width) // 2, (self.canvas.winfo_reqheight() - self.copy_of_image.height) // 2), image=self.photo_image, anchor=NW)
    
    def add_logo(self):
        logo_path = filedialog.askopenfilename()
        logo = Image.open(logo_path)
        resized_logo = Image.open(logo_path)
        
        # Resize the logo if needed
        max_logo_ratio = 0.2
        max_logo_size = (int(self.image.width * max_logo_ratio), int(self.image.height * max_logo_ratio))
        logo.thumbnail(max_logo_size, Image.LANCZOS)
        
        max_resized_logo_size = (int(self.copy_of_image.width * max_logo_ratio), int(self.copy_of_image.height * max_logo_ratio))
        resized_logo.thumbnail(max_resized_logo_size, Image.LANCZOS)
        
        # Paste the logo onto the image
        x = self.image.width - logo.width - 10
        y = self.image.height - logo.height - 10
        self.image.paste(logo, (x, y), logo)
        
        resized_x = self.copy_of_image.width - resized_logo.width - 10
        resized_y = self.copy_of_image.height - resized_logo.height - 10
        self.copy_of_image.paste(resized_logo, (resized_x, resized_y), resized_logo)
        
        # Update the canvas with the new image
        self.photo_image = ImageTk.PhotoImage(self.copy_of_image)
        self.canvas.create_image(0, 0, image=self.photo_image, anchor=NW)
    
    def save_image(self):
        saving_path = filedialog.asksaveasfilename(defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
        self.image.save(saving_path)
        self.canvas.delete("all")
        
    def detect_watermark(self):
        # Convert the canvas image to a numpy array
        img_np = np.array(self.copy_of_image)

        # Convert the image to grayscale
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

        # Apply a fixed threshold to segment the image
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

        # Find contours in the thresholded image
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw contours on the original image
        img_with_contours = img_np.copy()
        cv2.drawContours(img_with_contours, contours, -1, (0, 255, 0), 3)

        # Convert the image with contours back to PIL Image format
        img_with_contours_pil = Image.fromarray(img_with_contours)

        # Update the canvas with the image containing contours
        self.photo_image = ImageTk.PhotoImage(image=img_with_contours_pil)
        self.canvas.create_image(0, 0, image=self.photo_image, anchor=NW)

Watermarking()
        