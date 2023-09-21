import tkinter as tk

root = tk.Tk()
root.title("Text Alignment Example")

# Create a Label widget with left-aligned and top-aligned text
label = tk.Label(root, bg='blue', text="To", anchor="nw")

label.pack()

root.mainloop()
