import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Create the main tkinter window
root = tk.Tk()
root.title("Display Web Image in tkinter")
root.state('zoomed')
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Create a frame to hold the image
image_frame = tk.Frame(root)
image_frame.place(relx=0, rely=0, relheight=1, relwidth=1)
def imagen(widget):
    # Define the URL of the web image
    image_url = "https://m.media-amazon.com/images/M/MV5BMzI0NmVkMjEtYmY4MS00ZDMxLTlkZmEtMzU4MDQxYTMzMjU2XkEyXkFqcGdeQXVyMzQ0MzA0NTM@.jpg"  # Replace with the actual image URL

    # Download the image from the web
    response = requests.get(image_url)
    image_data = response.content

    # Create a PIL Image object from the image data
    image = Image.open(BytesIO(image_data))

    # Resize the image to match the frame's dimensions
    image = image.resize((screen_width, (screen_height)), Image.LANCZOS)

    # Create a PhotoImage object from the PIL Image
    photo = ImageTk.PhotoImage(image)
    return photo

# Create a label to display the image
image_label = tk.Label(image_frame, bg='blue')
image_label.place(relx=0.03, rely=0.04, relheight=0.4, relwidth=0.94)
photo =imagen(image_label)
image_label.config(image= photo)


# Start the tkinter main loop
root.mainloop()
