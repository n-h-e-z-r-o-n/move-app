import tkinter as tk

def close_window():
    root.destroy()

root = tk.Tk()

# Create a button to close the window
button = tk.Button(root, text="Close Window", command=close_window)
button.pack()

root.mainloop()