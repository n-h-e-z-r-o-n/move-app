import tkinter as tk
from PIL import Image, ImageEnhance, ImageTk

def adjust_brightness(image, factor):
    """
    Adjusts the brightness of an image by a given factor.
    """
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

def on_enter(event):
    global original_image
    # Increase brightness on hover (adjust the factor as needed)
    brightened_image = adjust_brightness(original_image, 1.5)
    label.config(image=brightened_image)
    label.image = brightened_image  # Update the reference to the image

def on_leave(event):
    label.config(image=original_image)
    label.image = original_image  # Restore the original image

root = tk.Tk()
root.geometry("400x400")

# Load your image
image = Image.open("your_image.png")  # Replace with your image file path
original_image = ImageTk.PhotoImage(image)

label = tk.Label(root, image=original_image)
label.pack()

# Bind mouse enter and leave events to the label
label.bind("<Enter>", on_enter)
label.bind("<Leave>", on_leave)

root.mainloop()
