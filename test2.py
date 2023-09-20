import tkinter as tk

class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master, placeholder, **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.insert(0, placeholder)

    def on_focus_in(self, event):
        if self.get() == self.placeholder:
            self.delete(0, "end")

    def on_focus_out(self, event):
        if self.get() == "":
            self.insert(0, self.placeholder)

root = tk.Tk()

entry = EntryWithPlaceholder(root, placeholder="Enter your name")
entry.pack()

root.mainloop()