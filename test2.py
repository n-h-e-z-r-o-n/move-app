import tkinter as tk
import requests
from PIL import Image, ImageTk
from io import BytesIO
import threading
import time
import clr
import multiprocessing

clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Threading')
from System import IntPtr, Int32, Func, Type, Environment
from System.Windows.Forms import Control
from System.Threading import Thread,ApartmentState,ThreadStart,SynchronizationContext,SendOrPostCallback
from System.Windows.Forms import Control
from System.Threading import Thread,ApartmentState,ThreadStart,SynchronizationContext,SendOrPostCallback

def imagen(image_url, screen_width, screen_height, widget):
    def load_image():
        thread_id = threading.get_ident()
        print(f"Thread ID2: {thread_id}")
        retry = 0
        while retry < 6:
            try:
                if image_url is None:
                    image = Image.open("./Default.png")
                else:

                    response = requests.get(image_url)
                    image_data = response.content
                    image = Image.open(BytesIO(image_data))

                image = image.resize((screen_width, screen_height), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                widget.config(image=photo)
                widget.image = photo  # Keep a reference to the PhotoImage to prevent it from being garbage collected
                break
            except requests.exceptions.RequestException as e:
                print(f"Error loading image: {e}")
                retry += 1
                time.sleep(5)


    image_thread = threading.Thread(target=load_image)
    image_thread.start()

def process(fun):
    process = multiprocessing.Process(target= fun)
    process.start()

def main():
    thread_id = threading.get_ident()
    print(f"Thread ID: {thread_id}")

    root = tk.Tk()

    image_label = tk.Label(root)
    image_label.pack()

    image_url = "https://m.media-amazon.com/images/M/MV5BNDllZjc2NjEtOGMwZS00ZmNkLTg2NDgtZjJkYjg0YjMxM2FmXkEyXkFqcGdeQXVyNzA5NjUyNjM@.jpg"  # Replace with your image URL
    screen_width = 1200  # Replace with your desired width
    screen_height = 1200  # Replace with your desired height

    # imagen(image_url, screen_width, screen_height, image_label)

    imagen(image_url, screen_height, screen_width, image_label)
    root.mainloop()

if __name__ == "__main__":
    t = Thread(ThreadStart(main))
    t.ApartmentState = ApartmentState.STA
    t.Start()
    t.Join()