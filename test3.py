import tkinter as tk
import time
from colorsys import rgb_to_hsv, hsv_to_rgb

def rgb_to_hex(rgb):
    """Convert RGB color tuple to hexadecimal string."""
    return "#{:02X}{:02X}{:02X}".format(*rgb)

def pulsing_color(label):


    for i in range(360):  # Transition through hue values (0 to 359)
        hue = i / 360.0
        rgb_color = hsv_to_rgb(hue, 1, 1)  # Convert hue to RGB
        hex_color = rgb_to_hex(tuple(int(val * 255) for val in rgb_color))

        label.config(bg=hex_color)
        label.update()  # Update the label's appearance
        time.sleep(0.01)  # Adjust the delay as needed for the desired pulsing speed
    root.after(1000, lambda :pulsing_color(label))

root = tk.Tk()
root.geometry("400x400")

label = tk.Label(root, text="Pulsing Color", width=20, height=5)
label.pack()

# Start the pulsing color effect
pulsing_color(label)

root.mainloop()
