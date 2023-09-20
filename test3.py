import tkinter as tk
from tkVideoPlayer import TkinterVideo

root = tk.Tk()

videoplayer = TkinterVideo(master=root, scaled=True)
videoplayer.load(r"C:\Users\HEZRON WEKESA\Videos\download.mp4")
videoplayer.pack(expand=True, fill="both")

videoplayer.play() # play the video

root.mainloop()