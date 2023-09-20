import tkinter as tk
import time
import colorsys





def pulsing_color(widget):
    for i in range(360):  # Transition through hue values (0 to 359)
        hue = i / 360.0
        rgb_color = tuple(int(val * 255) for val in colorsys.hsv_to_rgb(hue, 1, 1))   # Convert hue to RGB
        hex_color = "#{:02X}{:02X}{:02X}".format(*rgb_color)

        # Check if the color is not blue (#0000FF)
        if hex_color != "#0000FF":
            widget.config(bg=hex_color)
            widget.update()  # Update the label's appearance

        time.sleep(0.04)  # Adjust the delay as needed for the desired pulsing speed

    root.after(1000, lambda: pulsing_color(widget))


root = tk.Tk()
root.geometry("400x400")

label = tk.Label(root, text="Pulsing Colors", width=20, height=5)
label.pack()

# Start the pulsing color loop
pulsing_color(label)

root.mainloop()
