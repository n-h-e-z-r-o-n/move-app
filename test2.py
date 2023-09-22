import tkinter as tk

def on_double_click(event):
    print("Double-clicked on the frame")

root = tk.Tk()
root.title("Double-Click Event on Frame")

frame = tk.Frame(root, width=200, height=100, bg="lightgray")
frame.pack()

# Bind the double-click event to the frame
frame.bind("<Double-Button-1>", on_double_click)

root.mainloop()
