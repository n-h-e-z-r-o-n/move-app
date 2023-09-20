import tkinter as tk

root = tk.Tk()

# Create a Button widget with a raised border.
button1 = tk.Button(root, text="Raised", relief=tk.RAISED)

# Create a Button widget with a sunken border.
button2 = tk.Button(root, text="Sunken", relief=tk.SUNKEN)

# Create a Button widget with a flat border.
button3 = tk.Button(root, text="Flat", relief=tk.FLAT)

# Pack the buttons to the window.
button1.pack()
button2.pack()
button3.pack()

root.mainloop()