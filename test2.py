import tkinter as tk
from PIL import Image, ImageTk

# Create a tkinter window
root = tk.Tk()
root.geometry("400x400")

# Create a gradient image
width, height = 400, 400
gradient = Image.new("RGB", (width, height))

# Define the gradient colors (you can change these to create your desired gradient)
color1 = (255, 0, 0)  # Red
color2 = (0, 0, 255)  # Blue

for y in range(height):
    r = int(color1[0] + (color2[0] - color1[0]) * y / height)
    g = int(color1[1] + (color2[1] - color1[1]) * y / height)
    b = int(color1[2] + (color2[2] - color1[2]) * y / height)

    for x in range(width):
        gradient.putpixel((x, y), (r, g, b))

# Convert the gradient image to a PhotoImage
gradient_photo = ImageTk.PhotoImage(gradient)

# Create a label to display the gradient photo
label = tk.Label(root, image=gradient_photo)
label.pack()

root.mainloop()
