import tkinter as tk

root = tk.Tk()
root.geometry("300x200")

# Create a transparent LabelFrame
transparent_frame = tk.LabelFrame(root, text="Transparent LabelFrame", bg='green', bd=0, highlightthickness=0)
transparent_frame.place(relx=0.5, rely=0.5, anchor="center")

# Add a label inside the transparent LabelFrame
label = tk.Label(transparent_frame, text="Hello, World!")
label.pack()

root.mainloop()