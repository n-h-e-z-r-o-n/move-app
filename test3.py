import tkinter as tk

def change_brightness(widget, brightness):
    """Sets the brightness of the widget to the specified value."""
    widget.config(highlightbackground=widget.cget("highlightbackground")[:4] + str(brightness), highlightcolor=widget.cget("highlightcolor")[:4] + str(brightness))

# Create a Label widget.
label = tk.Label(text="This is a label.")

# Bind the change_brightness function to the Enter and Leave events of the label.
label.bind("<Enter>", lambda event: change_brightness(label, 1.5))
label.bind("<Leave>", lambda event: change_brightness(label, 1.0))

# Pack the label to the window.
label.pack()

root = tk.Tk()
root.mainloop()