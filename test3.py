import tkinter as tk

root = tk.Tk()

# Create a Label widget with an image and text displayed above each other.
label1 = tk.Label(root, compound=tk.TOP, text="This is some text.", image=tk.PhotoImage(file="image.gif"))
label1.pack()

# Create a Button widget with an image and text displayed to the left of each other.
button1 = tk.Button(root, compound=tk.LEFT, text="Click me!", image=tk.PhotoImage(file="image.gif"))
button1.pack()

root.mainloop()