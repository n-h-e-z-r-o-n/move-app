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

    # Ensure the image has an alpha channel.
    im = image.convert("RGBA")

    width, height = im.size
    pixels = im.load()

    # Define the top and bottom fade heights as a percentage of the image height.
    top_fade_height = int(height * 0.20)  # Adjust this value for the desired top fade height
    bottom_fade_height = int(height * 0.20)  # Adjust this value for the desired bottom fade height

    # Fade the top region to dark.
    for y in range(top_fade_height):
       alpha = int((y / top_fade_height) * 255)
    for x in range(width):
        pixels[x, y] = pixels[x, y][:3] + (alpha,)

    # Fade the bottom region to dark.
    for y in range(height - bottom_fade_height, height):
        alpha = int(((height - y) / bottom_fade_height) * 255)
    for x in range(width):
        pixels[x, y] = pixels[x, y][:3] + (alpha,)


    # Resize the image to match the frame's dimensions
    image = im.resize((4000, (400)), Image.LANCZOS)

    # Create a PhotoImage object from the PIL Image
    photo = ImageTk.PhotoImage(image)

    # Save the modified image.
    image.save('birdfade.png')

    return photo
proc()