import tkinter as tk





# Create the main tkinter window
root = tk.Tk()
root.title("Scrollable Frame Example")

# Create a Canvas widget to hold the frame and enable scrolling
canvas = tk.Canvas(root)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a Scrollbar and connect it to the Canvas
scrollbar = tk.Scrollbar(root, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.config(yscrollcommand=scrollbar.set)

# Create a frame to hold your content
frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor=tk.NW)

# Create a large frame within the canvas frame (replace this with your content)
large_frame = tk.Frame(frame, width=800, height=1900)
large_frame.pack()

# Add widgets and content to the large frame (replace this with your content)
# Example content:
label = tk.Label(large_frame, bg='green', text="This is a label in the large frame")
label.place(x = 0.1, rely=0.1, relheight = 0.1)


label2 = tk.Label(large_frame, bg='green',text="This is a label in the large frame")
label2.place(x = 0.1, rely=0.9, relheight = 0.1)

# Update the canvas scrolling region when the large frame changes size
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

frame.bind("<Configure>", on_frame_configure)





# Function to handle mouse wheel scrolling
def on_mouse_wheel(event):
    # Scroll the canvas up or down based on the mouse wheel direction
    if event.delta < 0:
        canvas.yview_scroll(1, "units")
    else:
        canvas.yview_scroll(-1, "units")
def on_touch_scroll(event):
    canvas.yview_scroll(-1 * event.delta, "units")

# Bind the mouse wheel event to the canvas
canvas.bind_all("<MouseWheel>", on_mouse_wheel)  # Bind touch scroll event if supported

# Bind touch screen scrolling event (using the <MouseWheel> event)
canvas.bind("<Enter>", lambda event: canvas.bind_all("<MouseWheel>", on_touch_scroll))
canvas.bind("<Leave>", lambda event: canvas.unbind_all("<MouseWheel>"))


# Start the tkinter main loop
root.mainloop()
