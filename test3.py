import tkinter as tk

root = tk.Tk()
root.geometry("300x200")

# Create a frame
frame2 = tk.Frame(root)
frame2.place(relheight=0.5, relwidth=0.5, rely=0.5, relx=0.5)

frame = tk.Frame(frame2)
frame.pack(fill=tk.BOTH, expand=True)

# Add a scroll bar
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create a text widget inside the frame
text_widget = tk.Text(frame, yscrollcommand=scrollbar.set)
text_widget.pack(fill=tk.BOTH, expand=True)

# Link the scroll bar to the text widget
scrollbar.config(command=text_widget.yview)

# Add some text to the text widget (just for demonstration)
for i in range(50):
    text_widget.insert(tk.END, f"This is line {i+1}\n")

root.mainloop()

FRAME_1 = tk.Frame(root, bg='black')
FRAME_1.place(relx=0, rely=0, relwidth=1, relheight=1)
FRAME_1_canvas = tk.Canvas(FRAME_1, borderwidth=0, highlightthickness=0, bg='black')
FRAME_1_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
FRAME_1_scrollbar = tk.Scrollbar(root, command=FRAME_1_canvas.yview)
FRAME_1_canvas.config(yscrollcommand=FRAME_1_scrollbar.set)
FRAME_1_screen = tk.Frame(FRAME_1_canvas, bg='black')
FRAME_1_canvas.create_window((0, 0), window=FRAME_1_screen, anchor=tk.NW)