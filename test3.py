import tkinter as tk

class VerticalScrolledFrame(tk.Frame):
    def __init__(self, parent, bg, *args, **kw):
        super().__init__(parent, *args, **kw)
        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0, bg=bg)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Create a frame inside the canvas
        self.interior = tk.Frame(self.canvas, height=2000, bg=bg)
        interior_id = self.canvas.create_window(0, 0, window=self.interior, anchor="nw")

        # Configure scroll region dynamically
        self.interior.bind("<Configure>", self._configure_interior)
        self.canvas.bind("<Configure>", self._configure_canvas)

        # Initialize scroll position
        self.scrollposition = 1
        self.prevy = 0

        # Bind touch events
        self.bind("<Enter>", lambda _: self.bind_all("<Button-1>", self.on_press), "+")
        self.bind("<Leave>", lambda _: self.unbind_all("<Button-1>"), "+")
        self.bind("<Enter>", lambda _: self.bind_all("<B1-Motion>", self.on_touch_scroll), "+")
        self.bind("<Leave>", lambda _: self.unbind_all("<B1-Motion>"), "+")

    def _configure_interior(self, event):
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canvas.config(scrollregion=f"0 0 {size[0]} {size[1]}")
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            self.canvas.config(width=self.interior.winfo_reqwidth())

    def _configure_canvas(self, event):
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())

    def on_press(self, event):
        self.offset_y = event.y_root
        if self.scrollposition < 1:
            self.scrollposition = 1
        elif self.scrollposition > self.interior.winfo_reqheight():
            self.scrollposition = self.interior.winfo_reqheight()
        self.canvas.yview_moveto(self.scrollposition / self.interior.winfo_reqheight())

    def on_touch_scroll(self, event):
        nowy = event.y_root
        sectionmoved = 15
        if nowy > self.prevy:
            event.delta = -sectionmoved
        elif nowy < self.prevy:
            event.delta = sectionmoved
        else:
            event.delta = 0
        self.prevy = nowy
        self.scrollposition += event.delta
        self.canvas.yview_moveto(self.scrollposition / self.interior.winfo_reqheight())

if __name__ == "__main__":
    root = tk.Tk()
    vsf = VerticalScrolledFrame(root, bg="white")
    vsf.grid(row=0, column=0, sticky="nsew")

    # Add widgets to the scrolled frame (e.g., labels, buttons)
    for row in range(50):
        tk.Label(vsf.interior, text=f"Row {row}").grid(row=row, column=0)

    root.mainloop()