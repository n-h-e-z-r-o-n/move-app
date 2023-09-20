import tkinter as tk
import requests
from PIL import Image, ImageTk, ImageFilter
from io import BytesIO

# Define the URL of the web image
image_url = "https://m.media-amazon.com/images/M/MV5BMzI0NmVkMjEtYmY4MS00ZDMxLTlkZmEtMzU4MDQxYTMzMjU2XkEyXkFqcGdeQXVyMzQ0MzA0NTM@.jpg"  # Replace with the actual image URL

# Download the image from the web
response = requests.get(image_url)
image_data = response.content

# Create a PIL Image object from the image data
image = Image.open(BytesIO(image_data))

# Assuming you have screen_width and screen_height defined earlier
screen_width = 800  # Replace with your actual screen dimensions
screen_height = 600

# Resize the image to match the frame's dimensions
image = image.resize((screen_width, screen_height), Image.LANCZOS)

# Create a gradient mask image
gradient = Image.new("L", (screen_width, screen_height))
for y in range(screen_height):
    alpha = int(255 * abs(y - (screen_height / 2)) / (screen_height / 2))
    gradient.putpixel((0, y), alpha)

# Apply the gradient as an alpha mask to the image
image.putalpha(gradient)

# Create a PhotoImage object from the PIL Image
photo = ImageTk.PhotoImage(image)

# Create a tkinter window
root = tk.Tk()

# Create a label to display the image
image_label = tk.Label(root, bg='blue')
image_label.pack()

# Set the image as the label's image
image_label.config(image=photo)

root.mainloop()
