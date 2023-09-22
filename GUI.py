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
from System.Threading import Thread, ApartmentState, ThreadStart

if not have_runtime():  # 没有webview2 runtime
    install_runtime()

is_fullscreen = False
placeholder_text = None
screen_width = None
screen_height = None
large_frame_size = None
root = None

import imdb

ia = imdb.Cinemagoer()


def on_frame_configure(widget, event):  # Update the canvas scrolling region when the large frame changes size
    widget.configure(scrollregion=widget.bbox("all"))


def change_bg_OnHover(widget, colorOnHover, colorOnLeave):  # Color change bg on Mouse Hover
    widget.bind("<Enter>", func=lambda e: widget.config(background=colorOnHover))
    widget.bind("<Leave>", func=lambda e: widget.config(background=colorOnLeave))


def change_fg_OnHover(widget, colorOnHover, colorOnLeave):  # Color change fg on Mouse Hover
    widget.bind("<Enter>", func=lambda e: widget.config(fg=colorOnHover))
    widget.bind("<Leave>", func=lambda e: widget.config(fg=colorOnLeave))


def on_mouse_wheel(widget, event):  # Function to handle mouse wheel scrolling
    # Scroll the canvas up or down based on the mouse wheel direction
    if event.delta < 0:
        widget.yview_scroll(1, "units")
    else:
        widget.yview_scroll(-1, "units")


def imagen(image_url, screen_width, screen_height):
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


def imagen_fade(poster_url, screen_height, screen_width):
    # Download the image from the web
    response = requests.get(poster_url)
    image_data = response.content
    # Create a PIL Image object from the image data
    image = Image.open(BytesIO(image_data))
    # Resize the image to match the frame's dimensions
    h = screen_height - 200
    image = image.resize((screen_width, (h)), Image.LANCZOS)
    # Ensure the image has an alpha channel.
    im = image.convert("RGBA")
    width, height = im.size
    pixels = im.load()
    # Define the top and bottom fade heights as a percentage of the image height.
    top_fade_height = int(height * 0.50)  # Adjust this value for the desired top fade height
    bottom_fade_height = int(height * 0.50)  # Adjust this value for the desired bottom fade height
    # Fade the top region to dark.
    for y in range(top_fade_height):
        alpha = int((y / top_fade_height) * 255)
        for x in range(width):
            pixels[x, y] = pixels[x, y][:3] + (alpha,)
    # Fade the bottom region to dark.
    for y in range(height - bottom_fade_height, height):
        alpha = int(((height - y) / bottom_fade_height) * 255)
        for x in range(width):
            pixels[x, y] = pixels[x, y][:3] + (alpha,)

    # Save the modified image.
    im.save('birdfade.png')
    # Create a PhotoImage object from the PIL Image
    photo = ImageTk.PhotoImage(im)
    return photo


def change_color(main_widget, widget):
    # Generate a random color in hexadecimal format (#RRGGBB)
    new_color = "#{:02X}{:02X}{:02X}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    widget.config(fg=new_color)  # Change the background color of the label

    # Schedule the function to run again in 1000 milliseconds (1 second)
    main_widget.after(1000, lambda: change_color(main_widget, widget))


def pulsing_color(main_widget, widget):
    for i in range(360):  # Transition through hue values (0 to 359)
        hue = i / 360.0
        rgb_color = tuple(int(val * 255) for val in colorsys.hsv_to_rgb(hue, 1, 1))  # Convert hue to RGB
        hex_color = "#{:02X}{:02X}{:02X}".format(*rgb_color)

        # Check if the color is not blue (#0000FF)
        if hex_color != "#0000FF":
            widget.config(bg=hex_color)
            widget.update()  # Update the label's appearance
        time.sleep(0.04)  # Adjust the delay as needed for the desired pulsing speed
    main_widget.after(3000, lambda: pulsing_color(widget))


def on_entry_click(widget, event):
    global placeholder_text
    if widget.get() == "Search":
        widget.delete(0, tk.END)
        widget.config(fg='white')  # Change text color to black


def on_focusout(widget, event):
    global placeholder_text
    if not widget.get():
        widget.insert(0, "Search")
        widget.config(fg='gray')  # Change text color to gray

def play(widget):
    print('not')
    widget.forget()
    widget.place(relx=0.03, rely=0.04, relheight=0.4, relwidth=0.94)
    original_x = widget.winfo_x()
    original_y = widget.winfo_y()
    original_width = widget.winfo_width()
    original_height = widget.winfo_height()
    fullscreen_button = tk.Button(widget, border=0, borderwidth=0, text="⤢", bg='black', justify='center', activebackground='black', activeforeground='white', fg='white', font=('Times New Roman', 25), command=lambda: toggle_fullscreen(root, widget, original_x, original_y, original_width, original_height))
    fullscreen_button.place(relx=0.97, rely=0.95, relheight=0.05, relwidth=0.03)


def toggle_fullscreen(main_widget,  widget, original_x, original_y, original_width, original_height):
    global is_fullscreen
    if is_fullscreen:
        # Restore the video frame to its original size and position
        main_widget.overrideredirect(False)
        widget.forget()
        widget.place(relx=0.03, rely=0.04, relheight=0.4, relwidth=0.94, x=original_x, y=original_y, width=original_width, height=original_height)
        is_fullscreen = False
    else:
        # Expand the video frame to full screen
        main_widget.overrideredirect(True)
        widget.forget()
        widget.place(relx=0, rely=0, x=0, y=0, relwidth=1, relheight=screen_height / large_frame_size)
        is_fullscreen = True


def main():
    global hold
    global is_fullscreen
    global placeholder_text
    global screen_width
    global screen_height
    global large_frame_size
    global root

    if not have_runtime():#没有webview2 runtime
        install_runtime()

    root = tk.Tk()
    root.title("Move App")
    root.state('zoomed')  # this creates a window that takes over the screen
    root.minsize(150, 100)

    # Get the screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    large_frame_size = screen_height + 700
    print(screen_width)
    print(screen_height)
    print(large_frame_size)

    # Create a Canvas widget to hold the frame and enable scrolling
    canvas = tk.Canvas(root, highlightthickness=0)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create a Scrollbar and connect it to the Canvas
    scrollbar = tk.Scrollbar(root, command=canvas.yview)
    # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.config(yscrollcommand=scrollbar.set)

    # Create a frame to hold your content of the canvers
    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor=tk.NW)

    frame.bind("<Configure>", lambda e: on_frame_configure(canvas, e))
    canvas.bind_all("<MouseWheel>", lambda e: on_mouse_wheel(canvas, e))  # Bind the mouse wheel event to the canvas
    canvas.configure(scrollregion=canvas.bbox("all"))  # Configure the canvas scrolling region to hide scrollbars





    # ------------

    movies = ia.search_movie('Avengers')
    ia.update(movies[0])  # Fetch additional details, including images

    def cast():
        i = 0
        cast_str = ''
        while i < len(movies[0]["cast"]):
            if len(movies[0]["cast"][i]) != 0 and i < 15:
                cast_str += str(movies[0]["cast"][i]) + ', '
            i += 1

        return cast_str

    def production():
        i = 0
        production_str = ''
        while i < len(movies[0]['production companies']):
            if len(movies[0]['production companies'][i]) != 0 and i < 5:
                production_str += str(movies[0]['production companies'][i]) + ', '
            i += 1
        return production_str

    def genres():
        genres_str = ''
        for i in movies[0]["genres"]:
            genres_str += str(i) + ', '
        return genres_str

    def country():
        country_str = ''
        for i in movies[0]["countries"]:
            country_str += str(i) + '. '
        return country_str

    def plot():
        plot_str = ''
        for i in movies[0]["plot"]:
            plot_str += str(i)
        return plot_str

    movie_id = movies[0].movieID
    movie_title = movies[0]['title']
    movie_ratting = movies[0]['rating']
    movie_type = movies[0]['kind']
    movie_country = country()
    movie_genres = genres()
    movie_year = movies[0]['year']
    movie_production_company = production()
    movie_cast_names = cast()
    movie_plot = plot()

    # (widget, movie_id, movie_title, movie_ratting, movie_type, movie_country, movie_genres, movie_year, movie_production_company, movie_cast_names, movie_plot, movie_poster_url)
    movie_poster_url = movies[0].get('full-size cover url')

    r1_title = movies[1]['title']
    r1_year = movies[1]['year']
    recomednation_1_poster = movies[1].get('full-size cover url')
    r2_title = movies[2]['title']
    r2_year = movies[2]['year']
    recomednation_2_poster = movies[2].get('full-size cover url')
    r3_title = movies[3]['title']
    r3_year = movies[3]['year']
    recomednation_3_poster = movies[3].get('full-size cover url')
    r4_title = movies[4]['title']
    r4_year = movies[4]['year']
    recomednation_4_poster = movies[4].get('full-size cover url')
    r5_title = movies[5]['title']
    r5_year = movies[5]['year']
    recomednation_5_poster = movies[5].get('full-size cover url')
    r6_title = movies[6]['title']
    r6_year = movies[6]['year']
    recomednation_6_poster = movies[6].get('full-size cover url')

    # (r1_title, r1_year, recomednation_1_poster, r2_title, r2_year, recomednation_2_poster, r3_title, r3_year, recomednation_3_poster, r4_title, r4_year, recomednation_4_poster, r5_title, r5_year, recomednation_5_poster, r6_title, r6_year, recomednation_6_poster )

    # ------------

    def watch_page(widget, movie_id, movie_title, movie_ratting, movie_type, movie_country, movie_genres, movie_year, movie_production_company, movie_cast_names, movie_plot, movie_poster_url, r1_title, r1_year, recomednation_1_poster, r2_title, r2_year, recomednation_2_poster, r3_title, r3_year, recomednation_3_poster, r4_title, r4_year, recomednation_4_poster, r5_title, r5_year, recomednation_5_poster, r6_title, r6_year, recomednation_6_poster):
        # Create a large frame within the canvas frame (replace this with your content)
        large_frame = tk.Frame(widget, bg='black', width=screen_width, height=large_frame_size)
        large_frame.pack(fill=tk.X)

        label3 = tk.Label(large_frame )
        label3.place(relx=0.04, rely=0.52, relheight=0.16, relwidth=0.13)
        poster = imagen(movie_poster_url, 250, 317)
        label3.config(image=poster)
        label3.image = poster

        color_bg = "black"

        Title = tk.Label(large_frame, bg=color_bg, fg='white', text=f"{movie_title}", justify=tk.LEFT, anchor=tk.W, font=('Algerian', 28))
        Title.place(relx=0.19, rely=0.52, relheight=0.025, relwidth=0.75)

        tk.Label(large_frame, bg=color_bg, fg='lightblue', text=f"HD", font=('Colonna MT', 24, 'bold')).place(relx=0.19, rely=0.549, relheight=0.015, relwidth=0.04)
        tk.Label(large_frame, bg=color_bg, fg='gray', text=f"✯✯✯✩", anchor=tk.E, font=('Arial Black', 20, 'bold')).place(relx=0.24, rely=0.549, relheight=0.015, relwidth=0.1)
        tk.Label(large_frame, bg=color_bg, fg='gray', text=f"{movie_ratting}", anchor=tk.SW, font=('Calibri', 16)).place(relx=0.34, rely=0.55, relheight=0.015, relwidth=0.04)

        Type1 = tk.Label(large_frame, bg=color_bg, fg='gray', text="Type : ", justify=tk.LEFT, anchor=tk.W, font=('Comic Sans MS', 12, "bold"))
        Type1.place(relx=0.19, rely=0.568, relheight=0.016, relwidth=0.06)

        Type11 = tk.Label(large_frame, bg=color_bg, fg='white', text=f"{movie_type}", justify=tk.LEFT, anchor=tk.W, font=('Comic Sans MS', 12, "bold"))
        Type11.place(relx=0.26, rely=0.568, relheight=0.016, relwidth=0.68)

        Type2 = tk.Label(large_frame, bg=color_bg, fg='gray', text="Country : ", justify=tk.LEFT, anchor=tk.W, font=('Comic Sans MS', 12, "bold"))
        Type2.place(relx=0.19, rely=0.586, relheight=0.016, relwidth=0.06)

        Type12 = tk.Label(large_frame, bg=color_bg, fg='white', text=movie_country, justify=tk.LEFT, anchor=tk.W, font=('Comic Sans MS', 12, "bold"))
        Type12.place(relx=0.26, rely=0.586, relheight=0.016, relwidth=0.68)

        Type3 = tk.Label(large_frame, bg=color_bg, fg='gray', text="Genre : ", justify=tk.LEFT, anchor=tk.W, font=('Comic Sans MS', 12, "bold"))
        Type3.place(relx=0.19, rely=0.604, relheight=0.016, relwidth=0.06)

        Type13 = tk.Label(large_frame, bg=color_bg, fg='white', text=movie_genres, justify=tk.LEFT, anchor=tk.W, font=('Comic Sans MS', 12, "bold"))
        Type13.place(relx=0.26, rely=0.604, relheight=0.016, relwidth=0.68)

        Type4 = tk.Label(large_frame, bg=color_bg, fg='gray', text="Release : ", justify=tk.LEFT, anchor=tk.W, font=('Comic Sans MS', 12, "bold"))
        Type4.place(relx=0.19, rely=0.622, relheight=0.016, relwidth=0.06)

        Type14 = tk.Label(large_frame, bg=color_bg, fg='white', text=f"{movie_year}", justify=tk.LEFT, anchor=tk.W, font=('Comic Sans MS', 12, "bold"))
        Type14.place(relx=0.26, rely=0.622, relheight=0.016, relwidth=0.68)

        Type5 = tk.Label(large_frame, bg=color_bg, fg='gray', text="Production : ", justify=tk.LEFT, anchor=tk.W, font=('Comic Sans MS', 12, "bold"))
        Type5.place(relx=0.19, rely=0.64, relheight=0.016, relwidth=0.06)

        Type15 = tk.Label(large_frame, bg=color_bg, fg='white', text=movie_production_company, justify=tk.LEFT, anchor=tk.W, font=('Comic Sans MS', 12, "bold"))
        Type15.place(relx=0.26, rely=0.64, relheight=0.016, relwidth=0.68)

        Type6 = tk.Label(large_frame, bg=color_bg, fg='gray', text="Cast : ", justify=tk.LEFT, anchor=tk.W, font=('Comic Sans MS', 12, "bold"))
        Type6.place(relx=0.19, rely=0.658, relheight=0.016, relwidth=0.06)

        Type16 = tk.Text(large_frame, bg=color_bg, fg='white', borderwidth=0, border=0, wrap=tk.WORD, font=('Comic Sans MS', 12))
        Type16.insert("1.0", movie_cast_names)
        Type16.config(state="disabled")
        Type16.place(relx=0.26, rely=0.658, relheight=0.026, relwidth=0.68)

        plot_wdget = tk.Text(large_frame, bg=color_bg, fg='gray', borderwidth=0, border=0, wrap=tk.WORD, font=('Comic Sans MS', 12))
        plot_wdget.insert("1.0", movie_plot)
        plot_wdget.config(state="disabled")
        plot_wdget.place(relx=0.04, rely=0.689, relheight=0.078, relwidth=0.95)

        #  content:

        image_label = tk.Button(large_frame, text='▷', bg='black', fg='white', borderwidth=0, border=0, activebackground='black', activeforeground='black', relief=tk.FLAT, font=('Arial Black', 76, 'bold'), command=lambda: play(video_box))
        image_label.place(relx=0, rely=0.0, relheight=0.5, relwidth=1)
        photo = imagen_fade(movie_poster_url, screen_height, screen_width)
        image_label.config(image=photo, compound=tk.CENTER)
        image_label.image = photo
        image_label.focus_set()
        change_fg_OnHover(image_label, 'Blue', 'white')
        change_color(root, image_label)

        def search_movie(event):
             print('search')

        Search_box = tk.Entry(large_frame, font=('Georgia', 15), justify='center',insertbackground="lightblue", borderwidth=0, border=0, bg='black', fg='white')
        Search_box.place(relx=0.30, rely=0.007, relheight=0.017, relwidth=0.4)
        placeholder_text = "Search"
        Search_box.insert(0, placeholder_text)
        Search_box.bind("<FocusIn>", lambda e: on_entry_click(Search_box, e))
        Search_box.bind("<FocusOut>", lambda e: on_focusout(Search_box, e))
        change_bg_OnHover(Search_box, '#010127', 'black')
        Search_box.bind("<Return>", search_movie)
        image_label.focus_set()

        recomendation_tubs_bg_color = 'black'
        hover_color = 'lightblue'
        text_color = 'gray'

        label2 = tk.Label(large_frame, bg=recomendation_tubs_bg_color, borderwidth=0, border=0)
        label2.place(relx=0.04, rely=0.78, relheight=0.2, relwidth=0.15)
        r1_bt1 = tk.Button(label2, bg=recomendation_tubs_bg_color, borderwidth=0, activebackground=hover_color, border=0)
        r1_bt1.place(relx=0, rely=0, relwidth=1, relheight=1)
        r1_img = imagen(recomednation_1_poster, 280, 396)
        r1_bt1.config(image=r1_img)
        r1_bt1.image = r1_img
        change_bg_OnHover(r1_bt1, hover_color, recomendation_tubs_bg_color)
        r1_bt2 = tk.Button(label2, borderwidth=0, border=0, bg=recomendation_tubs_bg_color, activeforeground=hover_color, activebackground=recomendation_tubs_bg_color, fg=text_color, text=f'{r1_title}\n{r1_year}', font=('Bahnschrift Light', 13, 'bold'))
        r1_bt2.place(relx=0, rely=0.8, relwidth=1, relheight=0.2)
        change_fg_OnHover(r1_bt2, hover_color, text_color)
        label2.focus_set()
        r1_bt1.focus_set()
        r1_bt2.focus_set()

        label3 = tk.Label(large_frame, bg=recomendation_tubs_bg_color, borderwidth=0, border=0)
        label3.place(relx=0.2, rely=0.78, relheight=0.2, relwidth=0.15)
        r2_bt1 = tk.Button(label3, bg=recomendation_tubs_bg_color, activebackground=hover_color, borderwidth=0, border=0)
        r2_bt1.place(relx=0, rely=0, relwidth=1, relheight=1)
        r2_img = imagen(recomednation_2_poster, 280, 396)
        r2_bt1.config(image=r2_img)
        r2_bt1.image = r2_img
        change_bg_OnHover(r2_bt1, hover_color, recomendation_tubs_bg_color)
        r2_bt2 = tk.Button(label3, borderwidth=0, border=0, bg=recomendation_tubs_bg_color, activeforeground=hover_color, activebackground=recomendation_tubs_bg_color, fg=text_color, text=f'{r2_title}\n{r2_year}', font=('Bahnschrift Light', 13, 'bold'))
        r2_bt2.place(relx=0, rely=0.8, relwidth=1, relheight=0.2)
        change_fg_OnHover(r2_bt2, hover_color, text_color)
        label3.focus_set()
        r2_bt1.focus_set()
        r2_bt2.focus_set()

        label4 = tk.Label(large_frame, bg=recomendation_tubs_bg_color, borderwidth=0, border=0)
        label4.place(relx=0.36, rely=0.78, relheight=0.2, relwidth=0.15)
        r3_bt1 = tk.Button(label4, bg=recomendation_tubs_bg_color, activebackground=hover_color, borderwidth=0, border=0)
        r3_bt1.place(relx=0, rely=0, relwidth=1, relheight=1)
        r3_img = imagen(recomednation_3_poster, 280, 396)
        r3_bt1.config(image=r3_img)
        r3_bt1.image = r3_img
        change_bg_OnHover(r3_bt1, hover_color, recomendation_tubs_bg_color)
        r3_bt2 = tk.Button(label4, borderwidth=0, border=0, bg=recomendation_tubs_bg_color, activeforeground=hover_color, activebackground=recomendation_tubs_bg_color, fg=text_color, text=f'{r3_title}\n{r3_year}', font=('Bahnschrift Light', 13, 'bold'))
        r3_bt2.place(relx=0, rely=0.8, relwidth=1, relheight=0.2)
        change_fg_OnHover(r3_bt2, hover_color, text_color)
        label4.focus_set()
        r3_bt1.focus_set()
        r3_bt2.focus_set()

        label5 = tk.Label(large_frame, bg=recomendation_tubs_bg_color, borderwidth=0, border=0)
        label5.place(relx=0.52, rely=0.78, relheight=0.2, relwidth=0.15)
        r4_bt1 = tk.Button(label5, bg=recomendation_tubs_bg_color, activebackground=hover_color, borderwidth=0, border=0)
        r4_bt1.place(relx=0, rely=0, relwidth=1, relheight=1)
        r4_img = imagen(recomednation_4_poster, 280, 396)
        r4_bt1.config(image=r4_img)
        r4_bt1.image = r4_img
        change_bg_OnHover(r4_bt1, hover_color, recomendation_tubs_bg_color)
        r4_bt2 = tk.Button(label5, borderwidth=0, border=0, bg=recomendation_tubs_bg_color, activeforeground=hover_color, activebackground=recomendation_tubs_bg_color, fg=text_color, text=f'{r4_title}\n{r4_year}', font=('Bahnschrift Light', 13, 'bold'))
        r4_bt2.place(relx=0, rely=0.8, relwidth=1, relheight=0.2)
        change_fg_OnHover(r4_bt2, hover_color, text_color)
        label5.focus_set()
        r4_bt1.focus_set()
        r4_bt2.focus_set()

        label6 = tk.Label(large_frame, bg=recomendation_tubs_bg_color, borderwidth=0, border=0)
        label6.place(relx=0.68, rely=0.78, relheight=0.2, relwidth=0.15)
        r5_bt1 = tk.Button(label6, bg=recomendation_tubs_bg_color, activebackground=hover_color, borderwidth=0, border=0)
        r5_bt1.place(relx=0, rely=0, relwidth=1, relheight=1)
        r5_img = imagen(recomednation_5_poster, 280, 396)
        r5_bt1.config(image=r5_img)
        r5_bt1.image = r5_img
        change_bg_OnHover(r5_bt1, hover_color, recomendation_tubs_bg_color)
        r5_bt2 = tk.Button(label6, borderwidth=0, border=0, bg=recomendation_tubs_bg_color, activeforeground=hover_color, activebackground=recomendation_tubs_bg_color, fg=text_color, text=f'{r5_title}\n{r5_year}', font=('Bahnschrift Light', 13, 'bold'))
        r5_bt2.place(relx=0, rely=0.8, relwidth=1, relheight=0.2)
        change_fg_OnHover(r5_bt2, hover_color, text_color)
        label6.focus_set()
        r5_bt1.focus_set()
        r5_bt2.focus_set()

        label7 = tk.Label(large_frame, bg=recomendation_tubs_bg_color, borderwidth=0, border=0)
        label7.place(relx=0.84, rely=0.78, relheight=0.2, relwidth=0.15)
        r6_bt1 = tk.Button(label7, bg=recomendation_tubs_bg_color, activebackground=hover_color, borderwidth=0, border=0)
        r6_bt1.place(relx=0, rely=0, relwidth=1, relheight=1)
        r6_img = imagen(recomednation_6_poster, 280, 396)
        r6_bt1.config(image=r6_img)
        r6_bt1.image = r6_img
        change_bg_OnHover(r6_bt1, hover_color, recomendation_tubs_bg_color)
        r6_bt2 = tk.Button(label7, borderwidth=0, border=0, bg=recomendation_tubs_bg_color, activeforeground=hover_color, activebackground=recomendation_tubs_bg_color, fg=text_color, text=f'{r6_title}\n{r6_year}', font=('Bahnschrift Light', 13, 'bold'))
        r6_bt2.place(relx=0, rely=0.8, relwidth=1, relheight=0.2)
        change_fg_OnHover(r6_bt2, hover_color, text_color)
        label7.focus_set()
        r6_bt1.focus_set()
        r6_bt2.focus_set()

        video_box = tk.Frame(large_frame, bg='black')
        #frame2 = WebView2(video_box, 500, 500)
        #frame2.load_url(f'https://vidsrc.to/embed/movie/tt{movie_id}')
        #frame2.pack(side='left', padx=0, fill='both', expand=True)


    watch_page(frame, movie_id, movie_title, movie_ratting, movie_type, movie_country, movie_genres, movie_year, movie_production_company, movie_cast_names, movie_plot, movie_poster_url, r1_title, r1_year, recomednation_1_poster, r2_title, r2_year, recomednation_2_poster, r3_title, r3_year, recomednation_3_poster, r4_title, r4_year, recomednation_4_poster, r5_title, r5_year, recomednation_5_poster, r6_title, r6_year, recomednation_6_poster)

    root.mainloop()


if __name__ == "__main__":
    main()
    '''
    t = Thread(ThreadStart(main))
    t.ApartmentState = ApartmentState.STA
    t.Start()
    t.Join()
    '''
