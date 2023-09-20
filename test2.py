import tkinter as tk
from tkinter import ttk

def on_button_click():
    print("Button clicked!")

root = tk.Tk()
root.title("Rounded Button Example")

# Create a custom style
style = ttk.Style()

# Configure the custom style to create a rounded button
style.configure("Rounded.TButton", borderwidth=0, relief="flat", padding=10, bordercolor="white", background="lightblue", highlightthickness=0)

# Create a button with the custom style
rounded_button = ttk.Button(root, text="Click Me", style="Rounded.TButton", command=on_button_click)
rounded_button.pack(padx=20, pady=10)

root.mainloop()
