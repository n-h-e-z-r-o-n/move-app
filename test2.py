import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO

def display_web_image():
    url = "https://m.media-amazon.com/images/M/MV5BMzI0NmVkMjEtYmY4MS00ZDMxLTlkZmEtMzU4MDQxYTMzMjU2XkEyXkFqcGdeQXVyMzQ0MzA0NTM@.jpg"  # Replace with the URL of your image
    response = requests.get(url)
    image_bytes = BytesIO(response.content)
    image = Image.open(image_bytes)

    # Resize the image to match the frame's dimensions
    image = image.resize((frame.winfo_width(), frame.winfo_height()), Image.LANCZOS)

    photo = ImageTk.PhotoImage(image)
    label.config(image=photo)
    label.image = photo  # Keep a reference to the image to prevent it from being garbage collected

root = tk.Tk()
root.title("Stretch Web Image to Fill Frame")

frame = ttk.Frame(root)
frame.pack(fill="both", expand=True)

label = ttk.Label(frame)
label.pack(fill="both", expand=True)

button = ttk.Button(root, text="Load Web Image", command=display_web_image)
button.pack()

root.mainloop()
