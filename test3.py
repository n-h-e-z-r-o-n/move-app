import numpy as np
from PIL import Image

# Load the image to be blended.
im = Image.open(r"C:\Users\HEZRON WEKESA\Pictures\20220819_083721.jpg")

# Ensure the image has an alpha channel.
im = im.convert("RGBA")

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

# Save the modified image.
im.save('birdfade.png')
