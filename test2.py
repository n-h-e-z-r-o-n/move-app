import tkinter as tk
from tkinter import PhotoImage

# Function to change the image
from PIL import ImageTk


def change_image():
    global current_image_index
    current_image_index = (current_image_index + 1) % len(images)  # Cycle through images
    label.config(image=images[current_image_index])

# Create a Tkinter window
root = tk.Tk()
root.title("Change Label Image")

# Load your images (replace these paths with your image file paths)
image_paths = ["1.jpg", "2.jpg"]

# Create PhotoImage objects for each image
images = ImageTk.PhotoImage("1.jpg")

# Initialize the index to show the first image
current_image_index = 0

# Create a label with the initial image
label = tk.Label(root, image=images)
label.pack()

# Create a button to change the image
change_button = tk.Button(root, text="Change Image", command=change_image)
change_button.pack()

root.mainloop()
