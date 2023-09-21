from PIL import Image, ImageEnhance

# Load the image
input_image_path = "input_image.jpg"
output_image_path = "output_image.jpg"
image =  Image.open(r"C:\Users\HEZRON WEKESA\Pictures\20220819_083721.jpg")

# Define the number of steps for the fade effect
num_steps = 10

# Create a list of images with gradually reduced brightness
fade_images = []
for step in range(num_steps + 1):
    # Adjust brightness using ImageEnhance
    brightness_factor = 1.0 - (step / num_steps)  # Decrease brightness
    enhanced_image = ImageEnhance.Brightness(image).enhance(brightness_factor)
    fade_images.append(enhanced_image)

# Save the faded images as a GIF or another format
fade_images[0].save(output_image_path, save_all=True, append_images=fade_images[1:], duration=100, loop=0)

