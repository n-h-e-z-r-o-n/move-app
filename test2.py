import tkinter as tk

def toggle_fullscreen():
    global is_fullscreen
    if is_fullscreen:
        root.attributes("-fullscreen", False)
        fullscreen_button.config(text="Expand to Full Screen")
        is_fullscreen = False
    else:
        root.attributes("-fullscreen", True)
        fullscreen_button.config(text="Restore")
        is_fullscreen = True

root = tk.Tk()
root.title("Toggle Frame to Full Screen")

# Create a Frame widget
frame = tk.Frame(root, width=800, height=600, bg="green")
frame.pack(fill=tk.BOTH, expand=True)

# Create a button to toggle full screen
fullscreen_button = tk.Button(root, text="Expand to Full Screen", command=toggle_fullscreen)
fullscreen_button.pack()

is_fullscreen = False

root.mainloop()
