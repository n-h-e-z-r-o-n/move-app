import tkinter as tk
from PIL import Image, ImageTk
import io, base64
import threading

def imagen_2(image_path, screen_width, screen_height, widget):  # image processing
    def load_image():
        try:
            image = Image.open(image_path)
        except Exception as e:
            try:
                image = Image.open(io.BytesIO(image_path))
            except Exception as e:
                print(e)
                binary_data = base64.b64decode(image_path)  # Decode the string
                image = Image.open(io.BytesIO(binary_data))

        image = image.resize((screen_width, screen_height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        widget.config(image=photo)
        widget.image = photo  # Keep a reference to the PhotoImage to prevent it from being garbage collected

    load_image()


C = tk.Tk()

screenwidth = C.winfo_screenwidth()
screenheight = C.winfo_screenheight()
start_w = 600
start_h = 400
C.minsize(start_w, start_h)
C.maxsize(start_w, start_h)
pos_w = int((screenwidth / 2) - (start_w / 2))
pos_h = int((screenheight / 2) - (start_h / 2))
C.geometry(f'+{pos_w}+{pos_h}')
C.config(bg='blue')


f1 = tk.Label(C, borderwidth=0, border=0)
f1.place(relx=0, rely=0, relheight=1, relwidth=1)
imagen_2("Assets/startup.jpg", start_w, start_h, f1)

F2 = tk.Button(f1, borderwidth=0, text='4454545',  font=(20))
F2.place(relx=0.1, rely=0.1, relheight=0.5, relwidth=0.5)
#imagen_2(r"C:\Users\HEZRON WEKESA\Downloads\1__2_-removebg-preview.png", start_w, start_h, F2)

C.mainloop()