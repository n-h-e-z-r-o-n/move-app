import tkinter as tk

def switch_focus():
    # Set focus to the button when it's clicked
    button.focus_set()

root = tk.Tk()
root.title("Switch Focus Example")

entry = tk.Entry(root)
entry.pack()

button = tk.Button(root, text="Switch Focus", command=switch_focus)
button.pack()

root.mainloop()
