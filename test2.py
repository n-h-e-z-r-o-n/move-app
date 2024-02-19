import tkinter as tk

def smooth_scroll(widget, increment):
    # Get the current scroll position
    current_scroll = float(widget.yview()[0])

    # Calculate the new scroll position
    new_scroll = max(0.0, min(1.0, current_scroll + increment))

    # Set the new scroll position
    widget.yview_moveto(new_scroll)

    # Repeat the process until the desired position is reached


# Create the main application window
root = tk.Tk()
root.geometry("400x300")

# Create a Text widget with some content
text = tk.Text(root)
text.insert("end", "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 20)
text.pack(fill="both", expand=True)

# Bind mousewheel events for scrolling
def on_mousewheel(event):
    # Determine the direction of the scroll
    if event.delta < 0:
        smooth_scroll(text, 0.1)  # Scroll down
    else:
        smooth_scroll(text, -0.1)  # Scroll up

text.bind("<MouseWheel>", on_mousewheel)

# Run the application
root.mainloop()
