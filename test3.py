# Define the URL of the web image
from io import BytesIO

import requests
from PIL import Image, ImageTk
screen_width = 1000
screen_height = 1000
def proc():
        image_url = "https://m.media-amazon.com/images/M/MV5BMzI0NmVkMjEtYmY4MS00ZDMxLTlkZmEtMzU4MDQxYTMzMjU2XkEyXkFqcGdeQXVyMzQ0MzA0NTM@.jpg"  # Replace with the actual image URL

        # Download the image from the web
        response = requests.get(image_url)
        image_data = response.content

        # Create a PIL Image object from the image data
        image = Image.open(BytesIO(image_data))

        # Resize the image to match the frame's dimensions
        image = image.resize((1000, (1000)), Image.LANCZOS)


        # Create a blank transparent image with the same dimensions
        faded_image = Image.new("RGBA", (screen_width, screen_height))

        # Define the fade heights based on percentages
        top_fade_height = int(screen_height * 0.20)
        bottom_fade_height = int(screen_height * 0.20)

        # Apply fading to the top region
        for y in range(top_fade_height):
            alpha = int((y / top_fade_height) * 255)
            for x in range(screen_width):
                pixel_color = image.getpixel((x, y))
                faded_image.putpixel((x, y), pixel_color + (alpha,))

        # Apply fading to the bottom region
        for y in range(screen_height - bottom_fade_height, screen_height):
            alpha = int(((screen_height - y) / bottom_fade_height) * 255)
            for x in range(screen_width):
                pixel_color = image.getpixel((x, y))
                faded_image.putpixel((x, y), pixel_color + (alpha,))

        # Create a PhotoImage object from the PIL Image
        photo = ImageTk.PhotoImage(faded_image)

        return photo




proc()