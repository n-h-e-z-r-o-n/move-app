import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import requests
from io import BytesIO

# Define screen width and height (you should set these values appropriately)



def create_gradient_mask(width, height):
    # Create a gradient mask image
    mask = Image.new("L", (width, height))

    # Create a gradient from black to white
    for y in range(height):
        alpha = int((y / height) * 255)
        mask.putpixel((width // 2, y), alpha)

    return mask

def apply_gradient(image, gradient_mask):
    # Apply the gradient mask to the image
    gradient = Image.new("RGBA", image.size)
    gradient.paste(image, (0, 0))

    # Create a transparent version of the image
    image = Image.new("RGBA", image.size)
    image.paste(gradient, (0, 0), gradient_mask)

    return image

def imagen(widget):
    # Define the URL of the web image
    image_url = "https://m.media-amazon.com/images/M/MV5BMzI0NmVkMjEtYmY4MS00ZDMxLTlkZmEtMzU4MDQxYTMzMjU2XkEyXkFqcGdeQXVyMzQ0MzA0NTM@.jpg"

    # Download the image from the web
    response = requests.get(image_url)
    image_data = response.content

    # Create a PIL Image object from the image data
    image = Image.open(BytesIO(image_data))

    # Resize the image to match the frame's dimensions
    image = image.resize((screen_width, screen_height), Image.LANCZOS)

    # Create a gradient mask for the top and bottom
    gradient_mask = create_gradient_mask(screen_width, screen_height)

    # Apply the gradient effect to the image
    image_with_gradient = apply_gradient(image, gradient_mask)

    # Create a PhotoImage object from the modified image
    photo = ImageTk.PhotoImage(image_with_gradient)

    return photo

# Create a tkinter window
root = tk.Tk()
root.geometry("800x600")

# Create a label to display the image
image_label = tk.Label(root, bg='blue')
image_label.place(relx=0.03, rely=0.04, relheight=0.4, relwidth=0.94)
photo = imagen(image_label)
image_label.config(image=photo)

root.mainloop()
