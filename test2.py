import tkinter as tk

def on_double_click(event):
    print("Double-clicked")

root = tk.Tk()
root.geometry("300x200")

frame = tk.Frame(root, bg="lightgray", width=200, height=100)
frame.pack(padx=50, pady=50)

frame.bind("<Double-Button-1>", on_double_click)

root.mainloop()



