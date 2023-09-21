import numpy as np
from PIL import Image

# Load the two images to be blended.
im  = Image.open(r"C:\Users\HEZRON WEKESA\Pictures\20220819_083721.jpg")

im.putalpha(255)
width, height = im.size
pixels = im.load()
for y in range(int(height*.55), int(height*.75)):
    alpha = 255-int((y - height*.55)/height/.20 * 255)
    for x in range(width):
        pixels[x, y] = pixels[x, y][:3] + (alpha,)
for y in range(y, height):
    for x in range(width):
        pixels[x, y] = pixels[x, y][:3] + (0,)
im.save('birdfade.png')