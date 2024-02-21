import tkinter as tk

def on_touch_drag(event):
    dx, dy = event.x - old_x, event.y - old_y
    canvas.yview_scroll(int(-dy / 10), "units")  # Adjust scroll speed as needed
    old_x, old_y = event.x, event.y

root = tk.Tk()
canvas = tk.Canvas(root, width=300, height=200)  # Adjust dimensions
canvas.pack()

frame = tk.Frame(canvas, width=500, height=400)  # Adjust size of scrollable content
frame.pack()

# Add your widgets to the frame

canvas.bind("<Button-1>", on_touch_drag)  # Bind to left-click/touch
old_x, old_y = 0, 0  # Initialize touch position tracking

root.mainloop()