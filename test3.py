import tkinter as tk

class ScrollbarFrame(tk.Frame):
    def __init__(self, parent, height, width):
        super().__init__(parent)
        self.height = height
        self.width = width

        # Create a vertical scrollbar
        self.v_scrollbar = tk.Scrollbar(self, orient="vertical")
        self.v_scrollbar.pack(side="right", fill="y")

        # Create a canvas for scrolling
        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff",
                                height=height, width=width)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Attach scrollbar action to canvas
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)
        self.v_scrollbar.configure(command=self.canvas.yview)

        # Create a frame inside the canvas
        self.scrolled_frame = tk.Frame(self.canvas, background=self.canvas.cget('bg'))
        self.canvas.create_window((0, 0), window=self.scrolled_frame, anchor="nw")

        # Configure scroll region dynamically
        self.scrolled_frame.bind("<Configure>", self.on_configure)
        self.scrolled_frame.bind("<Configure>", self.on_frame_configure)

    def on_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

if __name__ == "__main__":
    root = tk.Tk()
    sbf = ScrollbarFrame(root, height=500, width=1000)
    sbf.grid(row=0, column=0, sticky='nsew')

    # Add labels to the scrolled frame
    for row in range(50):
        tk.Label(sbf.scrolled_frame, text=f"{row}", width=3, borderwidth="1", relief="solid").grid(row=row, column=0)
        tk.Label(sbf.scrolled_frame, text=f"Second column for row {row}",
                 background=sbf.scrolled_frame.cget('bg')).grid(row=row, column=1)

    root.mainloop()