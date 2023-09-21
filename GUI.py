import colorsys
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import customtkinter
import random
import time

import clr
from tkwebview2.tkwebview2 import WebView2, have_runtime, install_runtime
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Threading')
from System.Windows.Forms import Control
from System.Threading import Thread,ApartmentState,ThreadStart

if not have_runtime():  # 没有webview2 runtime
    install_runtime()
global hold
is_fullscreen = False
placeholder_text = None


def main():
        global hold
        global is_fullscreen
        global placeholder_text

        root = tk.Tk()
        root.title("Move App")
        root.state('zoomed') # this creates a window that takes over the screen
        root.minsize(150, 100)

        # Get the screen dimensions
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        large_frame_size = screen_height+700

        # Create a Canvas widget to hold the frame and enable scrolling
        canvas = tk.Canvas(root, highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a Scrollbar and connect it to the Canvas
        scrollbar = tk.Scrollbar(root, command=canvas.yview)
        #scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.config(yscrollcommand=scrollbar.set)

        # Create a frame to hold your content of the canvers
        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor=tk.NW)

        # Create a large frame within the canvas frame (replace this with your content)
        large_frame = tk.Frame(frame, bg='gray', width=screen_width,  height=large_frame_size)
        large_frame.pack(fill=tk.X)

        def change_color(widget):
            # Generate a random color in hexadecimal format (#RRGGBB)
            new_color = "#{:02X}{:02X}{:02X}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            widget.config(fg=new_color)  # Change the background color of the label

            # Schedule the function to run again in 1000 milliseconds (1 second)
            root.after(1000, lambda: change_color(widget))

        def pulsing_color(widget):

            for i in range(360):  # Transition through hue values (0 to 359)
                hue = i / 360.0
                rgb_color = tuple(int(val * 255) for val in colorsys.hsv_to_rgb(hue, 1, 1))  # Convert hue to RGB
                hex_color = "#{:02X}{:02X}{:02X}".format(*rgb_color)

                # Check if the color is not blue (#0000FF)
                if hex_color != "#0000FF":
                    widget.config(bg=hex_color)
                    widget.update()  # Update the label's appearance


                time.sleep(0.04)  # Adjust the delay as needed for the desired pulsing speed

            root.after(3000, lambda: pulsing_color(widget))

        def change_bg_OnHover(button, colorOnHover, colorOnLeave):  # Color change bg on Mouse Hover
            button.bind("<Enter>", func=lambda e: button.config(background=colorOnHover))
            button.bind("<Leave>", func=lambda e: button.config(background=colorOnLeave))

        def change_fg_OnHover(button, colorOnHover, colorOnLeave):  # Color change fg on Mouse Hover
            button.bind("<Enter>", func=lambda e: button.config(fg=colorOnHover))
            button.bind("<Leave>", func=lambda e: button.config(fg=colorOnLeave))

        def on_frame_configure(event):  # Update the canvas scrolling region when the large frame changes size
            canvas.configure(scrollregion=canvas.bbox("all"))

        def on_mouse_wheel(event):  # Function to handle mouse wheel scrolling
            # Scroll the canvas up or down based on the mouse wheel direction
            if event.delta < 0:
                canvas.yview_scroll(1, "units")
            else:
                canvas.yview_scroll(-1, "units")

        def Load_Movie(widget, movie_id):
            global hold
            movie_id = 'tt8385148'
            frame2 = WebView2(widget, 500, 5000)
            hold = frame2
            frame2.load_url(f'https://vidsrc.to/embed/movie/{movie_id}')
            frame2.pack(side='left', padx=0, fill='both', expand=True)

        def toggle_fullscreen(widget):
            global is_fullscreen
            if is_fullscreen:
                # Restore the video frame to its original size and position
                root.overrideredirect(False)
                widget.forget()
                widget.place(relx=0.03, rely=0.04, relheight=0.4, relwidth=0.94, x=original_x, y=original_y, width=original_width, height=original_height)
                is_fullscreen = False
            else:
                # Expand the video frame to full screen
                root.overrideredirect(True)
                widget.forget()
                widget.place(relx=0, rely=0, x=0, y=0, relwidth=1, relheight=screen_height/large_frame_size)
                is_fullscreen = True

        def imagen(widget):
            # Define the URL of the web image
            image_url = "https://m.media-amazon.com/images/M/MV5BMzI0NmVkMjEtYmY4MS00ZDMxLTlkZmEtMzU4MDQxYTMzMjU2XkEyXkFqcGdeQXVyMzQ0MzA0NTM@.jpg"  # Replace with the actual image URL

            # Download the image from the web
            response = requests.get(image_url)
            image_data = response.content

            # Create a PIL Image object from the image data
            image = Image.open(BytesIO(image_data))

            # Resize the image to match the frame's dimensions
            image = image.resize((screen_width, (screen_height)), Image.LANCZOS)

            # Create a PhotoImage object from the PIL Image
            photo = ImageTk.PhotoImage(image)
            return photo

        def on_entry_click(widget, event):
            global placeholder_text
            if widget.get() == "Search":
                widget.delete(0, tk.END)
                widget.config(fg='black')  # Change text color to black

        def on_focusout(widget, event):
            global placeholder_text
            if not widget.get():
                widget.insert(0, "Search")
                widget.config(fg='gray')  # Change text color to gray
        def play(widget):
            widget.place(relx=0.03, rely=0.04, relheight=0.4, relwidth=0.94)


        #  content:

        image_label = tk.Button(large_frame, bg='blue', fg='white', borderwidth=0, border=0, activebackground='white', activeforeground='yellow', relief=tk.FLAT, font = ('Arial Black', 76))
        image_label.place(relx=0, rely=0.0, relheight=0.5, relwidth=1)
        photo = imagen(image_label)
        image_label.config(image=photo, compound=tk.CENTER, text='▷')
        #change_fg_OnHover(image_label,'Blue', 'white')
        change_color(image_label)

        Search_box =  tk.Entry(large_frame,  font = ('Georgia', 17), justify='center', borderwidth=0, border=0, fg='gray')
        Search_box.place(relx=0.30, rely=0.007, relheight=0.02, relwidth=0.4)
        placeholder_text = "Search"
        Search_box.insert(0, placeholder_text)
        Search_box.bind("<FocusIn>", lambda e: on_entry_click(Search_box, e))
        Search_box.bind("<FocusOut>", lambda e: on_focusout(Search_box, e))
        #pulsing_color(Search_box)




        video_box = tk.Frame(large_frame, bg='green')
        #video_box.place(relx=0.03, rely=0.04, relheight=0.4, relwidth=0.94)
        #Load_Movie(video_box, None)

        original_x = video_box.winfo_x()
        original_y = video_box.winfo_y()
        original_width = video_box.winfo_width()
        original_height = video_box.winfo_height()

        #video_box.forget()

        fullscreen_button = tk.Button(video_box, border=0, borderwidth=0, text="⤢",  bg='black', justify='center', activebackground='black', activeforeground='white',fg='white', font = ('Arial Black', 26),  command=lambda: toggle_fullscreen(video_box))
        fullscreen_button.place(relx=0.97, rely=0.95, relheight=0.05, relwidth=0.03)





        label2 = tk.Button(large_frame, bg='green',text="This is a label in the large frame", command=lambda:hold.full_screeen())
        label2.place(x = 0.1, rely=0.7, relheight = 0.1)



        frame.bind("<Configure>", on_frame_configure)










        canvas.bind_all("<MouseWheel>", on_mouse_wheel)  # Bind the mouse wheel event to the canvas

        # Configure the canvas scrolling region to hide scrollbars
        canvas.configure(scrollregion=canvas.bbox("all"))




        root.mainloop()

if __name__ == "__main__":
    t = Thread(ThreadStart(main))
    t.ApartmentState = ApartmentState.STA
    t.Start()
    t.Join()
