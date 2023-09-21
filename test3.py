# Define the URL of the web image
from io import BytesIO

import requests
from PIL import Image, ImageTk

def proc():
        image_url = "https://m.media-amazon.com/images/M/MV5BMzI0NmVkMjEtYmY4MS00ZDMxLTlkZmEtMzU4MDQxYTMzMjU2XkEyXkFqcGdeQXVyMzQ0MzA0NTM@.jpg"  # Replace with the actual image URL

        # Download the image from the web
        response = requests.get(image_url)
        image_data = response.content

        # Create a PIL Image object from the image data
        image = Image.open(BytesIO(image_data))

        # Resize the image to match the frame's dimensions
        image = image.resize((1000, (1000)), Image.LANCZOS)

        





proc()