import tkinter as tk
from tkinter import PhotoImage

def create_gradient_image(width, height, color1, color2):
    """
    Create a gradient image with the specified width, height, and colors.
    """
    gradient_image = tk.PhotoImage(width=width, height=height)

    for x in range(width):
        r = int((color1[0] * (width - x) + color2[0] * x) / width)
        g = int((color1[1] * (width - x) + color2[1] * x) / width)
        b = int((color1[2] * (width - x) + color2[2] * x) / width)

        pixel_color = f'#{r:02x}{g:02x}{b:02x}'
        gradient_image.put(pixel_color, (x, 0))

    return gradient_image

root = tk.Tk()
root.title("Gradient Photo")

# Create a gradient image
gradient_color1 = (255, 0, 0)  # Red
gradient_color2 = (0, 0, 255)  # Blue
gradient_width = 400
gradient_height = 300
gradient_image = create_gradient_image(gradient_width, gradient_height, gradient_color1, gradient_color2)

# Create a label to display the gradient image
gradient_label = tk.Label(root, image=gradient_image)
gradient_label.place(relx=0.03, rely=0.04, relheight=0.4, relwidth=0.94)
root.mainloop()

