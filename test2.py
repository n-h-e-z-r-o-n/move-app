from PIL import Image, ImageTk, ImageDraw
import tkinter as tk
import requests
from io import BytesIO

# Replace with your actual screen dimensions
screen_width = 800
screen_height = 600

# Create a tkinter window
root = tk.Tk()
root.geometry(f"{screen_width}x{screen_height}")

# Create a frame to hold the image
image_frame = tk.Frame(root)
image_frame.pack(fill=tk.BOTH, expand=True)

def imagen(widget):
    # Define the URL of the web image
    image_url = "https://m.media-amazon.com/images/M/MV5BMzI0NmVkMjEtYmY4MS00ZDMxLTlkZmEtMzU4MDQxYTMzMjU2XkEyXkFqcGdeQXVyMzQ0MzA0NTM@.jpg"  # Replace with the actual image URL

    # Download the image from the web
    response = requests.get(image_url)
    image_data = response.content

    # Create a PIL Image object from the image data
    image = Image.open(BytesIO(image_data))

    # Resize the image to match the frame's dimensions
    image = image.resize((screen_width, screen_height), Image.LANCZOS)

    # Create a gradient mask image
    gradient = Image.new('L', (screen_width, screen_height))
    draw = ImageDraw.Draw(gradient)

    # Define the rainbow/gay colors
    rainbow_colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 128, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)]

    # Define the height of the gradient region
    gradient_height = int(screen_height * 0.2)

    # Create a gradient effect
    for i, color in enumerate(rainbow_colors):
        top = i * gradient_height
        bottom = (i + 1) * gradient_height
        draw.rectangle([0, top, screen_width, bottom], fill=color)

    # Paste the gradient over the original image
    image.paste(gradient, (0, 0), gradient)

    # Create a PhotoImage object from the modified PIL Image
    photo = ImageTk.PhotoImage(image)
    return photo

# Create a label to display the image
image_label = tk.Label(image_frame, bg='blue')
image_label.place(relx=0.03, rely=0.04, relheight=0.4, relwidth=0.94)
photo = imagen(image_label)
image_label.config(image=photo)

root.mainloop()
