import cv2
import numpy as np

# Load the image
image_path = 'your_image.jpg'
image = cv2.imread(image_path)

# Define the number of steps for the fading effect (more steps for smoother transition)
num_steps = 100

# Loop through the steps and decrease brightness gradually
for step in range(num_steps):
    # Calculate the alpha value for blending
    alpha = 1.0 - (step / num_steps)

    # Create a copy of the original image
    faded_image = image.copy()

    # Multiply each pixel by the alpha value to decrease brightness
    faded_image = cv2.multiply(faded_image, np.array([alpha]))

    # Display the faded image (you can save it to a file instead)
    cv2.imshow('Fading Image', faded_image)

    # Wait for a short time to display the fading effect
    cv2.waitKey(20)

# Close the window when done
cv2.destroyAllWindows()
