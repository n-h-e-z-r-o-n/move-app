import tkinter as tk

def change_cursor_color():
    entry.config(insertbackground="red")

root = tk.Tk()
root.title("Change Entry Cursor Color")

entry = tk.Entry(root)
entry.pack()

button = tk.Button(root, text="Change Cursor Color", command=change_cursor_color)
button.pack()

root.mainloop()
