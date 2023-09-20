import tkinter as tk
import random


def change_color(widget):
    # Generate a random color in hexadecimal format (#RRGGBB)
    new_color = "#{:02X}{:02X}{:02X}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    widget.config(bg=new_color)  # Change the background color of the label

    # Schedule the function to run again in 1000 milliseconds (1 second)
    root.after(1000, lambda : change_color(widget))


root = tk.Tk()
root.geometry("400x400")

label = tk.Label(root, text="Changing Color", width=20, height=5)
label.pack()

# Start the color-changing loop
change_color(label)

root.mainloop()
