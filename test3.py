import tkinter as tk

root = tk.Tk()

# Create a Label widget with an image and text displayed above each other.
label1 = tk.Label(root, bg='green', compound=tk.CENTER, text="This is some text.", image=tk.PhotoImage(file=r"C:\Users\HEZRON WEKESA\Pictures\12.png"))
label1.pack()

# Create a Button widget with an image and text displayed to the left of each other.
button1 = tk.Button(root, compound=tk.BOTTOM, text="Click me!", image=tk.PhotoImage(file=r"C:\Users\HEZRON WEKESA\Pictures\12.png"))
button1.pack()

root.mainloop()