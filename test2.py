import tkinter as tk

def on_entry_click(event):
    if entry.get() == "Placeholder Text":
        entry.delete(0, tk.END)
        entry.config(fg='black')  # Change text color to black

def on_focusout(event):
    if not entry.get():
        entry.insert(0, "Placeholder Text")
        entry.config(fg='gray')  # Change text color to gray

root = tk.Tk()
root.geometry("300x200")

placeholder_text = "Placeholder Text"

entry = tk.Entry(root, fg='gray')  # Set the initial text color to gray
entry.insert(0, placeholder_text)
entry.bind("<FocusIn>", lambda: on_entry_click(entry))
entry.bind("<FocusOut>", on_focusout)
entry.pack()

root.mainloop()
