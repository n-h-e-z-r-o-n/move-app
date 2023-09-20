import tkinter as tk

# Define a function to increase brightness
def increase_brightness(event):
    widget = event.widget
    widget.config(bg='lightblue')  # Change the background color to a brighter color

# Define a function to reset brightness
def reset_brightness(event):
    widget = event.widget
    widget.config(bg='blue')  # Reset the background color to the original color

root = tk.Tk()
root.geometry("400x400")

# Create a label widget
label = tk.Label(root, text="Hover over me!", bg='blue', font=('Arial', 18))
label.pack(pady=50)

# Bind the mouse enter event to increase_brightness function
label.bind("<Enter>", increase_brightness)

# Bind the mouse leave event to reset_brightness function
label.bind("<Leave>", reset_brightness)

root.mainloop()
