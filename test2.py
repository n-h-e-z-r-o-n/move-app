import tkinter as tk

def toggle_fullscreen(widget):
    global is_fullscreen
    if is_fullscreen:
        # Restore the video frame to its original size and position
        video_frame.place(x=original_x, y=original_y)
        video_frame.config(width=original_width, height=original_height)
        fullscreen_button.config(text="Expand to Full Screen")
        is_fullscreen = False
    else:
        # Expand the video frame to full screen
        video_frame.place(x=0, y=0)
        video_frame.config(width=root.winfo_screenwidth(), height=root.winfo_screenheight())
        fullscreen_button.config(text="Restore")
        is_fullscreen = True

root = tk.Tk()
root.title("Toggle Video Frame Full Screen")

# Create a frame to hold the video (replace this with your video widget)
video_frame = tk.Frame(root, bg="black", width=800, height=600)  # Replace with your video widget
video_frame.pack()

# Save the original size and position of the video frame
original_x = video_frame.winfo_x()
original_y = video_frame.winfo_y()
original_width = video_frame.winfo_width()
original_height = video_frame.winfo_height()

# Create a button to toggle full screen
fullscreen_button = tk.Button(root, text="Expand to Full Screen", command=toggle_fullscreen)
fullscreen_button.pack()

is_fullscreen = False

root.mainloop()
