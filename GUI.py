import colorsys
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import PhotoImage
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
top_search_page = None
top_watch_page = None
top_frame_main = None
widget_track_position = []
page_count = -1
search_q = None
root = None
FRAME_1_canvas = canvas_FRAME_2 = FRAME_1 = FRAME_2 = None
large_frame_size = None

from imdbmovies import IMDB
import imdb

ia = imdb.Cinemagoer()

imdb_other = IMDB()


def clean_url(url):
    url = url
    url = url.replace('_V1_', '_V1000_')  # Replace '_V1_' with '_V1000_'
    url = url.replace('_UX67_', '_UX1000_')  # Replace '_UX67_' with '_UX1000_'
    url = url.replace('_UY98_', '_UY1000_')
    url = url.replace('_CR0,0,67,98_', '_CR0,0,0,0_')  # Replace '_CR0,0,67,98_' with '_CR0,0,0,0_'
    url = url.replace('_CR5,0,67,98_', '_CR0,0,0,0_')  # Replace '_CR5,0,67,98_' with '_CR0,0,0,0_'
    url = url.replace('_CR1,0,67,98_', '_CR0,0,0,0_')  # Replace '_CR1,0,67,98_' with '_CR0,0,0,0_'
    return url

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


def widget_scroll_bind(widget):
    widget.bind("<Configure>", lambda e: on_frame_configure(widget, e))
    widget.bind_all("<MouseWheel>", lambda e: on_mouse_wheel(widget, e))


def imagen(image_url, screen_width, screen_height):
    if image_url is None:
        image = (Image.open("./Default.png"))
    else:  # Download the image from the web
        response = requests.get(image_url)
        image_data = response.content
        image = Image.open(BytesIO(image_data))  # Create a PIL Image object from the image data

    image = image.resize((screen_width, (screen_height)), Image.LANCZOS)  # Resize the image to match the frame's dimensions
    photo = ImageTk.PhotoImage(image)  # Create a PhotoImage object from the PIL Image
    return photo


def imagen_fade(poster_url, screen_height, screen_width):
    if poster_url is None:
        image = (Image.open("./Default.png"))
    else:
        # Download the image from the web
        response = requests.get(poster_url)
        image_data = response.content
        image = Image.open(BytesIO(image_data)) # Create a PIL Image object from the image data

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
    if widget.get() == "Search" or widget.get().isspace():
        widget.delete(0, tk.END)
        widget.config(fg='white')  # Change text color to black


def on_focusout(widget, event):
    if not widget.get() or widget.get().isspace():
        widget.delete(0, tk.END)
        widget.insert(0, "Search")
        widget.config(fg='gray')  # Change text color to gray


def play(widget):
    global root
    print('not')
    widget.forget()
    widget.place(relx=0.03, rely=0.04, relheight=0.4, relwidth=0.94)
    original_x = widget.winfo_x()
    original_y = widget.winfo_y()
    original_width = widget.winfo_width()
    original_height = widget.winfo_height()
    fullscreen_button = tk.Button(widget, border=0, borderwidth=0, text="⤢", bg='black', justify='center', activebackground='black', activeforeground='white', fg='white', font=('Times New Roman', 25), command=lambda: toggle_fullscreen(root, widget, original_x, original_y, original_width, original_height))
    fullscreen_button.place(relx=0.97, rely=0.95, relheight=0.05, relwidth=0.03)


def toggle_fullscreen(main_widget, widget, original_x, original_y, original_width, original_height):
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



def selected_movie_detail(movie_id):
    global top_frame_main, Home_frame, large_frame_size


    movies = ia.get_movie(movie_id)

    # ia.update(movies)
    def cast():
        i = 0
        cast_str = ''
        while i < len(movies["cast"]):
            if len(movies["cast"][i]) != 0 and i < 15:
                cast_str += str(movies["cast"][i]) + ', '
            i += 1

        return cast_str

    def production():
        i = 0
        production_str = ''
        while i < len(movies['production companies']):
            if len(movies['production companies'][i]) != 0 and i < 5:
                production_str += str(movies['production companies'][i]) + ', '
            i += 1
        return production_str

    def genres():
        genres_str = ''
        for i in movies["genres"]:
            genres_str += str(i) + ', '
        return genres_str

    def country():
        country_str = ''
        for i in movies["countries"]:
            country_str += str(i) + '. '
        return country_str

    def plot():
        plot_str = ''
        for i in movies["plot"]:
            plot_str += str(i)

        index_of_full_stop = plot_str.find('.')
        # Check if a full stop was found and print accordingly
        if index_of_full_stop != -1:
            plot_str = plot_str[:index_of_full_stop + 1]  # Include the full stop

        return plot_str

    def relese_year(move_choice):
        try:
            year = move_choice['year']
        except:
            try:
                year = ia.get_movie(move_choice.movieID).data['series years']
            except:
                year = ''
        return year

    movie_id = movies.movieID
    movie_title = movies['title']
    try:
        movie_ratting = movies['rating']
    except:
        movie_ratting = 'N\A'

    movie_type = movies['kind']
    try:
        movie_country = country()
    except:
        movie_country = 'N\A'
    try:
        movie_genres = genres()
    except:
        movie_genres = ''
    try:
        movie_year = relese_year(movies)
    except:
        movie_year = ''
    try:
        movie_production_company = production()
    except:
        movie_production_company = 'N\A'
    try:
        movie_cast_names = cast()
    except:
        movie_cast_names = 'N\A'
    try:
        movie_plot = plot()
    except:
        movie_plot = ''

    # cover_url = movies['cover url']
    # languages = movies['languages']
    # original_title = movies['original title']

    movie_poster_url = movies.get('full-size cover url')

    related_other = ia.search_movie(movie_title)
    if len(related_other) > 7:
            r1_title = related_other[1]['title']
            r1_year = relese_year(related_other[1])
            recomednation_1_poster = related_other[1].get('full-size cover url')
            r1_id = related_other[1].movieID

            r2_title = related_other[2]['title']
            r2_year = relese_year(related_other[2])
            recomednation_2_poster = related_other[2].get('full-size cover url')
            r2_id = related_other[2].movieID

            r3_title = related_other[3]['title']
            r3_year = relese_year(related_other[3])
            recomednation_3_poster = related_other[3].get('full-size cover url')
            r3_id = related_other[3].movieID

            r4_title = related_other[4]['title']
            r4_year = relese_year(related_other[4])
            recomednation_4_poster = related_other[4].get('full-size cover url')
            r4_id = related_other[4].movieID

            r5_title = related_other[5]['title']
            r5_year = relese_year(related_other[5])
            recomednation_5_poster = related_other[5].get('full-size cover url')
            r5_id = related_other[5].movieID

            r6_title = related_other[6]['title']
            r6_year = relese_year(related_other[6])
            recomednation_6_poster = related_other[6].get('full-size cover url')
            r6_id = related_other[6].movieID
    else:
        random_numbers = [random.randint(1, 50) for _ in range(6)]
        popular_movies_dic = imdb_other.popular_movies(genre=None, start_id=1, sort_by=None) # returns top 50 popular movies starting from start id
        r1_title = popular_movies_dic['results'][random_numbers[0]]['name']
        r1_year = popular_movies_dic['results'][random_numbers[0]]['year']
        recomednation_1_poster = popular_movies_dic['results'][random_numbers[0]]['poster']
        r1_id = popular_movies_dic['results'][random_numbers[0]]['id'].strip('t')

        r2_title = popular_movies_dic['results'][random_numbers[1]]['name']
        r2_year = popular_movies_dic['results'][random_numbers[1]]['year']
        recomednation_2_poster = popular_movies_dic['results'][random_numbers[1]]['poster']
        r2_id = popular_movies_dic['results'][random_numbers[1]]['id'].strip('t')

        r3_title = popular_movies_dic['results'][random_numbers[2]]['name']
        r3_year = popular_movies_dic['results'][random_numbers[2]]['year']
        recomednation_3_poster = popular_movies_dic['results'][random_numbers[2]]['poster']
        r3_id = popular_movies_dic['results'][random_numbers[2]]['id'].strip('t')

        r4_title = popular_movies_dic['results'][random_numbers[3]]['name']
        r4_year = popular_movies_dic['results'][random_numbers[3]]['year']
        recomednation_4_poster = popular_movies_dic['results'][random_numbers[3]]['poster']
        r4_id = popular_movies_dic['results'][random_numbers[3]]['id'].strip('t')

        r5_title = popular_movies_dic['results'][random_numbers[4]]['name']
        r5_year = popular_movies_dic['results'][random_numbers[4]]['year']
        recomednation_5_poster = popular_movies_dic['results'][random_numbers[4]]['poster']
        r5_id = popular_movies_dic['results'][random_numbers[4]]['id'].strip('t')

        r6_title = popular_movies_dic['results'][random_numbers[5]]['name']
        r6_year = popular_movies_dic['results'][random_numbers[5]]['year']
        recomednation_6_poster = popular_movies_dic['results'][random_numbers[5]]['poster']
        r6_id = popular_movies_dic['results'][random_numbers[5]]['id'].strip('t')




    """
    print("title", movie_title)
    print("kind", movie_type)
    print("year", movie_country)
    print("countries", movie_country)
    print("rating", movie_ratting)
    print('movie_poster_url', movie_poster_url)
    print("ID", movie_id)
    print("Year:", movie_year)
    print("Plot:", movie_plot)
    print("Genres:", movie_genres)
    print("Cast:", movie_cast_names)

    print('\n')
    print("r1_title", r1_title)
    print("r1_year", r1_year)
    print("recomednation_1_poster", recomednation_1_poster)
    print('\n')
    print("r2_title", r2_title)
    print("r2_year", r2_year)
    print("recomednation_2_poster", recomednation_2_poster)
    print('\n')
    print("r3_title", r3_title)
    print("r3_year", r3_year)
    print("recomednation_3_poster", recomednation_3_poster)
    print('\n')
    print("r4_title", r4_title)
    print("r4_year", r4_year)
    print("recomednation_4_poster", recomednation_4_poster)
    print('\n')
    print("r5_title", r5_title)
    print("r5_year", r5_year)
    print("recomednation_5_poster", recomednation_5_poster)
    print('\n')
    print("r6_title", r6_title)
    print("r6_year", r6_year)
    print("recomednation_6_poster", recomednation_6_poster)
    """

    # movie_id, movie_title, movie_ratting, movie_type, movie_country, movie_genres, movie_year, movie_production_company, movie_cast_names, movie_plot, movie_poster_url, r1_title, r1_year, recomednation_1_poster, r2_title, r2_year, recomednation_2_poster, r3_title, r3_year, recomednation_3_poster, r4_title, r4_year, recomednation_4_poster, r5_title, r5_year, recomednation_5_poster, r6_title, r6_year, recomednation_6_poster
    # r1_id, r2_id, r3_id, r4_id, r5_id, r6_id
    watch_page(top_frame_main, movie_id, movie_title, movie_ratting, movie_type, movie_country, movie_genres, movie_year, movie_production_company, movie_cast_names, movie_plot, movie_poster_url, r1_title, r1_year, recomednation_1_poster, r2_title, r2_year, recomednation_2_poster, r3_title, r3_year, recomednation_3_poster, r4_title, r4_year, recomednation_4_poster, r5_title, r5_year, recomednation_5_poster, r6_title, r6_year, recomednation_6_poster, r1_id, r2_id, r3_id, r4_id, r5_id, r6_id)


def watch_page(widget, movie_id, movie_title, movie_ratting, movie_type, movie_country, movie_genres, movie_year, movie_production_company, movie_cast_names, movie_plot, movie_poster_url, r1_title, r1_year, recomednation_1_poster, r2_title, r2_year, recomednation_2_poster, r3_title, r3_year, recomednation_3_poster, r4_title, r4_year, recomednation_4_poster, r5_title, r5_year, recomednation_5_poster, r6_title, r6_year, recomednation_6_poster, r1_id, r2_id, r3_id, r4_id, r5_id, r6_id):
    global screen_width
    global screen_height
    global large_frame_size
    global top_frame_main
    global widget_track_position, search_q
    global page_count, FRAME_1, FRAME_2, canvas_FRAME_2, FRAME_1_canvas

    FRAME_2.tkraise()
    widget_scroll_bind(canvas_FRAME_2)

    # Create a large frame within the canvas frame (replace this with your content)
    large_frame = tk.Frame(widget, bg='black', width=screen_width, height=large_frame_size)
    large_frame.place(relwidth=1, relheight=1, relx=0, rely=0)
    widget_track_position.append(large_frame)
    large_frame.tkraise()
    page_count += 1

    label3 = tk.Label(large_frame)
    label3.place(relx=0.04, rely=0.52, relheight=0.16, relwidth=0.13)
    #poster = imagen(movie_poster_url, 250, 317)
    #label3.config(image=poster)
    #label3.image = poster

    color_bg = "black"

    Title_wdget = tk.Label(large_frame, bg=color_bg, fg='white', text=f"{movie_title}", justify=tk.LEFT, anchor=tk.W, font=('Algerian', 28))
    Title_wdget.place(relx=0.19, rely=0.52, relheight=0.025, relwidth=0.75)

    tk.Label(large_frame, bg=color_bg, fg='lightblue', text=f"HD", font=('Colonna MT', 24, 'bold')).place(relx=0.19, rely=0.549, relheight=0.015, relwidth=0.04)
    tk.Label(large_frame, bg=color_bg, fg='gray', text=f"✯✯✯✩", anchor=tk.E, font=('Arial Black', 20, 'bold')).place(relx=0.24, rely=0.549, relheight=0.015, relwidth=0.1)
    tk.Label(large_frame, bg=color_bg, fg='gray', text=f"{movie_ratting}", anchor=tk.SW, font=('Calibri', 16)).place(relx=0.34, rely=0.55, relheight=0.015, relwidth=0.04)

    Type1_wdget = tk.Label(large_frame, bg=color_bg, fg='gray', text="Type : ", justify=tk.LEFT, anchor=tk.W, font=('Comic Sans MS', 12, "bold"))
    Type1_wdget.place(relx=0.19, rely=0.568, relheight=0.016, relwidth=0.06)

    Type2_wdget = tk.Label(large_frame, bg=color_bg, fg='white', text=f"{movie_type}", justify=tk.LEFT, anchor=tk.W, font=('Comic Sans MS', 12))
    Type2_wdget.place(relx=0.26, rely=0.568, relheight=0.016, relwidth=0.68)

    Country1_wdget = tk.Label(large_frame, bg=color_bg, fg='gray', text="Country : ", justify=tk.LEFT, anchor=tk.W, font=('Comic Sans MS', 12, "bold"))
    Country1_wdget.place(relx=0.19, rely=0.586, relheight=0.016, relwidth=0.06)

    Country2_wdget = tk.Label(large_frame, bg=color_bg, fg='white', text=movie_country, justify=tk.LEFT, anchor=tk.W, font=('Comic Sans MS', 12,))
    Country2_wdget.place(relx=0.26, rely=0.586, relheight=0.016, relwidth=0.68)

    Genre1_wdget = tk.Label(large_frame, bg=color_bg, fg='gray', text="Genre : ", justify=tk.LEFT, anchor=tk.W, font=('Comic Sans MS', 12, "bold"))
    Genre1_wdget.place(relx=0.19, rely=0.604, relheight=0.016, relwidth=0.06)

    Genre2_wdget = tk.Label(large_frame, bg=color_bg, fg='white', text=movie_genres, justify=tk.LEFT, anchor=tk.W, font=('Comic Sans MS', 12))
    Genre2_wdget.place(relx=0.26, rely=0.604, relheight=0.016, relwidth=0.68)

    Release_date1_wdget = tk.Label(large_frame, bg=color_bg, fg='gray', text="Release : ", justify=tk.LEFT, anchor=tk.W, font=('Comic Sans MS', 12, "bold"))
    Release_date1_wdget.place(relx=0.19, rely=0.622, relheight=0.016, relwidth=0.06)

    Release_date2_wdget = tk.Label(large_frame, bg=color_bg, fg='white', text=f"{movie_year}", justify=tk.LEFT, anchor=tk.W, font=('Comic Sans MS', 12))
    Release_date2_wdget.place(relx=0.26, rely=0.622, relheight=0.016, relwidth=0.68)

    Production1_wdget = tk.Label(large_frame, bg=color_bg, fg='gray', text="Production : ", justify=tk.LEFT, anchor=tk.W, font=('Comic Sans MS', 12, "bold"))
    Production1_wdget.place(relx=0.19, rely=0.64, relheight=0.016, relwidth=0.06)

    Production2_wdget = tk.Label(large_frame, bg=color_bg, fg='white', text=movie_production_company, justify=tk.LEFT, anchor=tk.W, font=('Comic Sans MS', 12))
    Production2_wdget.place(relx=0.26, rely=0.64, relheight=0.016, relwidth=0.68)

    Cast1_wdget = tk.Label(large_frame, bg=color_bg, fg='gray', text="Cast : ", justify=tk.LEFT, anchor=tk.W, font=('Comic Sans MS', 12, "bold"))
    Cast1_wdget.place(relx=0.19, rely=0.658, relheight=0.016, relwidth=0.06)

    Cast2_wdget = tk.Text(large_frame, bg=color_bg, fg='white', borderwidth=0, border=0, wrap=tk.WORD, font=('Comic Sans MS', 12))
    Cast2_wdget.insert("1.0", movie_cast_names)
    Cast2_wdget.config(state="disabled")
    Cast2_wdget.place(relx=0.26, rely=0.658, relheight=0.026, relwidth=0.68)

    plot_wdget = tk.Text(large_frame, bg=color_bg, fg='gray', borderwidth=0, border=0, wrap=tk.WORD, font=('Comic Sans MS', 12))
    plot_wdget.insert("1.0", movie_plot)
    plot_wdget.config(state="disabled")
    plot_wdget.place(relx=0.04, rely=0.689, relheight=0.035, relwidth=0.95)

    plot_wdget1 = tk.Text(large_frame, bg='green', fg='gray', borderwidth=0, border=0, wrap=tk.WORD, font=('Comic Sans MS', 12))
    plot_wdget1.place(relx=0.04, rely=0.727, relheight=0.037, relwidth=0.95)

    #  content:

    image_label = tk.Button(large_frame, text='▷', bg='black', fg='white', borderwidth=0, border=0, activebackground='black', activeforeground='yellow', relief=tk.FLAT, font=('Arial Black', 76, 'bold'), command=lambda: play(video_box))
    image_label.place(relx=0, rely=0.0, relheight=0.5, relwidth=1)
    #photo = imagen_fade(movie_poster_url, screen_height, screen_width)
    #image_label.config(image=photo, compound=tk.CENTER)
    #image_label.image = photo
    change_fg_OnHover(image_label, 'Blue', 'white')
    #change_color(root, image_label)

    back_tracking_widget = tk.Button(large_frame, font=('Georgia', 20), justify='center', fg='gray', text='⤽', activebackground='black', activeforeground='yellow', borderwidth=0, border=0, bg='black', command=previous_back_track_page_display)
    back_tracking_widget.place(relx=0, rely=0, relheight=0.017, relwidth=0.021)
    change_fg_OnHover(back_tracking_widget, 'yellow', 'gray')

    froward_tracking_widget = tk.Button(large_frame, font=('Georgia', 20), justify='center', fg='gray', text='⤼', activebackground='black', activeforeground='yellow', borderwidth=0, border=0, bg='black', command=previous_forwad_track_page_display)
    froward_tracking_widget.place(relx=0.021, rely=0, relheight=0.017, relwidth=0.021)
    change_fg_OnHover(froward_tracking_widget, 'yellow', 'gray')

    Search_box = tk.Entry(large_frame, font=('Georgia', 15), justify='center',   insertbackground="lightblue", borderwidth=0, border=0, bg='black', fg='white')
    Search_box.place(relx=0.30, rely=0.007, relheight=0.017, relwidth=0.4)
    Search_box.insert(0, 'Search')
    Search_box.bind("<FocusIn>", lambda e: on_entry_click(Search_box, e))
    Search_box.bind("<FocusOut>", lambda e: on_focusout(Search_box, e))
    change_bg_OnHover(Search_box, '#010127', 'black')
    Search_box.bind("<Return>", lambda event: search_movies_request(top_frame_main, Search_box, event))

    recomendation_tubs_bg_color = '#1A2421'
    hover_color = 'lightblue'
    text_color = 'gray'

    label2 = tk.Label(large_frame, bg=recomendation_tubs_bg_color, borderwidth=0, border=0)
    label2.place(relx=0.04, rely=0.78, relheight=0.2, relwidth=0.15)
    r1_bt1 = tk.Button(label2, bg=recomendation_tubs_bg_color, borderwidth=0, activebackground=hover_color, border=0, command=lambda id=r1_id: selected_movie_detail(id))
    r1_bt1.place(relx=0, rely=0, relwidth=1, relheight=1)
    # r1_img = imagen(recomednation_1_poster, 280, 396)
    # r1_bt1.config(image=r1_img)
    # r1_bt1.image = r1_img
    change_bg_OnHover(r1_bt1, hover_color, recomendation_tubs_bg_color)
    r1_bt2 = tk.Button(label2, borderwidth=0, border=0, bg=recomendation_tubs_bg_color, activeforeground=hover_color, activebackground=recomendation_tubs_bg_color, fg=text_color, text=f'{r1_title}\n{r1_year}', font=('Calibri', 11, 'bold'), command=lambda id=r1_id: selected_movie_detail(id))
    r1_bt2.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)
    change_fg_OnHover(r1_bt2, hover_color, text_color)

    label3 = tk.Label(large_frame, bg=recomendation_tubs_bg_color, borderwidth=0, border=0)
    label3.place(relx=0.2, rely=0.78, relheight=0.2, relwidth=0.15)
    r2_bt1 = tk.Button(label3, bg=recomendation_tubs_bg_color, activebackground=hover_color, borderwidth=0, border=0, command=lambda id=r2_id: selected_movie_detail(id))
    r2_bt1.place(relx=0, rely=0, relwidth=1, relheight=1)
    # r2_img = imagen(recomednation_2_poster, 280, 396)
    # r2_bt1.config(image=r2_img)
    # r2_bt1.image = r2_img
    change_bg_OnHover(r2_bt1, hover_color, recomendation_tubs_bg_color)
    r2_bt2 = tk.Button(label3, borderwidth=0, border=0, bg=recomendation_tubs_bg_color, activeforeground=hover_color, activebackground=recomendation_tubs_bg_color, fg=text_color, text=f'{r2_title}\n{r2_year}', font=('Calibri', 11, 'bold'), command=lambda id=r2_id: selected_movie_detail(id))
    r2_bt2.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)
    change_fg_OnHover(r2_bt2, hover_color, text_color)

    label4 = tk.Label(large_frame, bg=recomendation_tubs_bg_color, borderwidth=0, border=0)
    label4.place(relx=0.36, rely=0.78, relheight=0.2, relwidth=0.15)
    r3_bt1 = tk.Button(label4, bg=recomendation_tubs_bg_color, activebackground=hover_color, borderwidth=0, border=0, command=lambda id=r3_id: selected_movie_detail(id))
    r3_bt1.place(relx=0, rely=0, relwidth=1, relheight=1)
    # r3_img = imagen(recomednation_3_poster, 280, 396)
    # r3_bt1.config(image=r3_img)
    # r3_bt1.image = r3_img
    change_bg_OnHover(r3_bt1, hover_color, recomendation_tubs_bg_color)
    r3_bt2 = tk.Button(label4, borderwidth=0, border=0, bg=recomendation_tubs_bg_color, activeforeground=hover_color, activebackground=recomendation_tubs_bg_color, fg=text_color, text=f'{r3_title}\n{r3_year}', font=('Calibri', 11, 'bold'), command=lambda id=r3_id: selected_movie_detail(id))
    r3_bt2.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)
    change_fg_OnHover(r3_bt2, hover_color, text_color)

    label5 = tk.Label(large_frame, bg=recomendation_tubs_bg_color, borderwidth=0, border=0)
    label5.place(relx=0.52, rely=0.78, relheight=0.2, relwidth=0.15)
    r4_bt1 = tk.Button(label5, bg=recomendation_tubs_bg_color, activebackground=hover_color, borderwidth=0, border=0, command=lambda id=r4_id: selected_movie_detail(id))
    r4_bt1.place(relx=0, rely=0, relwidth=1, relheight=1)
    # r4_img = imagen(recomednation_4_poster, 280, 396)
    # r4_bt1.config(image=r4_img)
    # r4_bt1.image = r4_img
    change_bg_OnHover(r4_bt1, hover_color, recomendation_tubs_bg_color)
    r4_bt2 = tk.Button(label5, borderwidth=0, border=0, bg=recomendation_tubs_bg_color, activeforeground=hover_color, activebackground=recomendation_tubs_bg_color, fg=text_color, text=f'{r4_title}\n{r4_year}', font=('Calibri', 11, 'bold'), command=lambda id=r4_id: selected_movie_detail(id))
    r4_bt2.place(relx=0, rely=0.8, relwidth=1, relheight=0.1)
    change_fg_OnHover(r4_bt2, hover_color, text_color)

    label6 = tk.Label(large_frame, bg=recomendation_tubs_bg_color, borderwidth=0, border=0)
    label6.place(relx=0.68, rely=0.78, relheight=0.2, relwidth=0.15)
    r5_bt1 = tk.Button(label6, bg=recomendation_tubs_bg_color, activebackground=hover_color, borderwidth=0, border=0, command=lambda id=r5_id: selected_movie_detail(id))
    r5_bt1.place(relx=0, rely=0, relwidth=1, relheight=1)
    # r5_img = imagen(recomednation_5_poster, 280, 396)
    # r5_bt1.config(image=r5_img)
    # r5_bt1.image = r5_img
    change_bg_OnHover(r5_bt1, hover_color, recomendation_tubs_bg_color)
    r5_bt2 = tk.Button(label6, borderwidth=0, border=0, bg=recomendation_tubs_bg_color, activeforeground=hover_color, activebackground=recomendation_tubs_bg_color, fg=text_color, text=f'{r5_title}\n{r5_year}', font=('Calibri', 11, 'bold'), command=lambda id=r5_id: selected_movie_detail(id))
    r5_bt2.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)
    change_fg_OnHover(r5_bt2, hover_color, text_color)

    label7 = tk.Label(large_frame, bg=recomendation_tubs_bg_color, borderwidth=0, border=0)
    label7.place(relx=0.84, rely=0.78, relheight=0.2, relwidth=0.15)
    r6_bt1 = tk.Button(label7, bg=recomendation_tubs_bg_color, activebackground=hover_color, borderwidth=0, border=0, command=lambda id=r6_id: selected_movie_detail(id))
    r6_bt1.place(relx=0, rely=0, relwidth=1, relheight=1)
    # r6_img = imagen(recomednation_6_poster, 280, 396)
    # r6_bt1.config(image=r6_img)
    # r6_bt1.image = r6_img
    change_bg_OnHover(r6_bt1, hover_color, recomendation_tubs_bg_color)
    r6_bt2 = tk.Button(label7, borderwidth=0, border=0, bg=recomendation_tubs_bg_color, activeforeground=hover_color, activebackground=recomendation_tubs_bg_color, fg=text_color, text=f'{r6_title}\n{r6_year}', font=('Calibri', 11, 'bold'), command=lambda id=r6_id: selected_movie_detail(id))
    r6_bt2.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)
    change_fg_OnHover(r6_bt2, hover_color, text_color)

    # video_box = tk.Frame(large_frame, bg='black')
    # frame2 = WebView2(video_box, 500, 500)
    # frame2.load_url(f'https://vidsrc.to/embed/movie/tt{movie_id}')
    # frame2.pack(side='left', padx=0, fill='both', expand=True)


# watch_page(frame, movie_id, movie_title, movie_ratting, movie_type, movie_country, movie_genres, movie_year, movie_production_company, movie_cast_names, movie_plot, movie_poster_url, r1_title, r1_year, recomednation_1_poster, r2_title, r2_year, recomednation_2_poster, r3_title, r3_year, recomednation_3_poster, r4_title, r4_year, recomednation_4_poster, r5_title, r5_year, recomednation_5_poster, r6_title, r6_year, recomednation_6_poster)

def search_movies_request(widget, user_query, event):

    user_search_query = user_query.get()
    search_results = ia.search_movie(user_search_query)
    print(len(search_results))
    total_results = len(search_results)
    movie_list = []
    for movie in search_results:
        title = movie['title']
        movie_id = movie.movieID
        try:
            year = movie['year']
        except:
            try:
                year = ia.get_movie(movie_id).data['series years']
            except:
                year = ''

        post_url = movie.get('full-size cover url')
        movie_list.append((title, year, post_url, movie_id))

    Search_result(widget, movie_list)


def previous_back_track_page_display():
    global page_count, widget_track_position,  FRAME_1, FRAME_2, FRAME_1_canvas, canvas_FRAME_2
    if page_count > 0:
        page_count -= 1
        if page_count == 0:
            print('FRAME_1')
            FRAME_1.tkraise()
            widget_scroll_bind(FRAME_1_canvas)
        else:
            print('FRAME_2')
            FRAME_2.tkraise()
            widget_scroll_bind(canvas_FRAME_2)

        print('page_count: ', page_count)
        print(widget_track_position[page_count])
        widget_track_position[page_count].tkraise()
        print('back')


def previous_forwad_track_page_display():
    global page_count, widget_track_position,  FRAME_1, FRAME_2,  FRAME_1_canvas, canvas_FRAME_2
    if page_count < (len(widget_track_position) - 1):
        page_count += 1
        if page_count == 0:
            print('FRAME_1')
            FRAME_1.tkraise()
            widget_scroll_bind(FRAME_1_canvas)
        else:
            print('FRAME_2')
            FRAME_2.tkraise()
            widget_scroll_bind(canvas_FRAME_2)


        print('page_count: ', page_count)
        widget_track_position[page_count].tkraise()

        print('frowd')


def Search_result(widget, m_list):
    global top_search_page, widget_track_position, page_count, top_frame_main, search_q, FRAME_1, FRAME_2, canvas_FRAME_2, large_frame_size
    FRAME_2.tkraise()
    widget_scroll_bind(canvas_FRAME_2)

    movie_list_grid = []
    Search_result_frame = tk.Frame(widget, bg='black', width=screen_width, height=large_frame_size)
    Search_result_frame.place(relwidth=1, relheight=1, relx=0, rely=0)
    Search_result_frame.tkraise()
    widget_track_position.append(Search_result_frame)
    page_count += 1

    back_tracking_widget = tk.Button(Search_result_frame, font=('Georgia', 20), justify='center', fg='gray', text='⤽', activebackground='black', activeforeground='yellow', borderwidth=0, border=0, bg='black', command=previous_back_track_page_display)
    back_tracking_widget.place(relx=0, rely=0, relheight=0.017, relwidth=0.021)
    change_fg_OnHover(back_tracking_widget, 'yellow', 'gray')

    froward_tracking_widget = tk.Button(Search_result_frame, font=('Georgia', 20), justify='center', fg='gray', text='⤼', activebackground='black', activeforeground='yellow', borderwidth=0, border=0, bg='black', command=previous_forwad_track_page_display)
    froward_tracking_widget.place(relx=0.021, rely=0, relheight=0.017, relwidth=0.021)
    change_fg_OnHover(froward_tracking_widget, 'yellow', 'gray')

    Search_box = tk.Entry(Search_result_frame, font=('Georgia', 15), justify='center', insertbackground="lightblue", borderwidth=0, border=0, bg='black', fg='white')
    Search_box.place(relx=0.30, rely=0.007, relheight=0.017, relwidth=0.4)
    placeholder_text = "Search"
    Search_box.insert(0, placeholder_text)
    Search_box.bind("<FocusIn>", lambda e: on_entry_click(Search_box, e))
    Search_box.bind("<FocusOut>", lambda e: on_focusout(Search_box, e))
    change_bg_OnHover(Search_box, '#010127', 'black')
    Search_box.bind("<Return>", lambda event: search_movies_request(top_frame_main, Search_box, event))

    recomendation_tubs_bg_color = 'black'
    hover_color = 'lightblue'

    def grid(widget, movies_list_result, total_movies, track):
        print("passed", track)
        global hold
        for i in movie_list_grid:
            i.destroy()
        i_high = int(large_frame_size * 0.2) - 10
        i_widh = int(screen_width * 0.15) - 10
        print("i_high :", i_high)
        print("i_widh :", i_widh)
        current_widgets = 0
        column = 0
        row = 0
        x_pos = 0.04
        y_pos = 0.04
        while row < 4:
            if track == total_movies:
                break
            while column < 6:
                if track == total_movies:
                    break
                label1 = tk.Label(widget, bg=recomendation_tubs_bg_color, borderwidth=0, border=0)
                label1.place(relx=x_pos, rely=y_pos, relheight=0.2, relwidth=0.15)
                r1_bt1 = tk.Button(label1, bg='#1A2421', borderwidth=0, activebackground=hover_color, border=0, command=lambda id=movies_list_result[track][3]: selected_movie_detail(id))
                r1_bt1.place(relx=0, rely=0, relwidth=1, relheight=1)
                # r1_img = imagen(movies_list_result[track][2], 280, 396)
                r1_img = imagen(movies_list_result[track][2], i_widh, i_high)
                r1_bt1.config(image=r1_img)
                r1_bt1.image = r1_img
                change_bg_OnHover(r1_bt1, hover_color, '#1A2421')
                r1_bt2 = tk.Button(label1, borderwidth=0, border=0, bg=recomendation_tubs_bg_color, activeforeground=hover_color, activebackground=recomendation_tubs_bg_color, fg='gray', text=f'{movies_list_result[track][0]}\n{movies_list_result[track][1]}', font=('Calibri', 11), command=lambda id=movies_list_result[track][3]: selected_movie_detail(id))
                r1_bt2.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)
                change_fg_OnHover(r1_bt2, hover_color, 'gray')
                movie_list_grid.append(label1)

                x_pos += 0.16
                column += 1
                track += 1
                current_widgets += 1

            column = 0
            x_pos = 0.04
            y_pos += 0.21
            row += 1

        print(total_movies, ' --- ', track)
        print(total_movies - track)
        print('cw -', current_widgets)

        if (total_movies - track) > 0:
            pages = tk.Button(Search_result_frame, bg=recomendation_tubs_bg_color, font=('Colonna MT', 15, 'bold'), activebackground=recomendation_tubs_bg_color,
                              activeforeground='green', text="next", fg='gray', justify=tk.CENTER, borderwidth=0, border=0)
            pages.config(command=lambda a=Search_result_frame, b=movies_list_result, c=total_movies, d=track: grid(a, b, c, d))
            pages.place(rely=0.91, relx=0.4, relheight=0.02, relwidth=0.09)
            movie_list_grid.append(pages)
            change_fg_OnHover(pages, 'lightblue', 'gray')

        if track > 24:
            print('preve ', track)
            track = track - (current_widgets + 24)
            pages1 = tk.Button(Search_result_frame, bg=recomendation_tubs_bg_color, font=('Colonna MT', 15, 'bold'), activebackground=recomendation_tubs_bg_color,
                               activeforeground='green', text="previous", fg='gray', justify=tk.CENTER, borderwidth=0, border=0)
            pages1.config(command=lambda a=Search_result_frame, b=movies_list_result, c=total_movies, d=track: grid(a, b, c, d))
            pages1.place(rely=0.91, relx=0.5, relheight=0.02, relwidth=0.09)
            movie_list_grid.append(pages1)
            change_fg_OnHover(pages1, 'lightblue', 'gray')

    grid(Search_result_frame, m_list, len(m_list), 0)

def Home_Page(widget):
        global widget_track_position, page_count, screen_height, screen_width, canvas_FRAME_2, FRAME_1_canvas, top_frame_main

        FRAME_1.tkraise()
        widget_scroll_bind(FRAME_1_canvas)
        Home_frame_hight = screen_height * 5

        # Section 1 ===============================================================================

        Suggestion = tk.Frame(widget,  borderwidth=0, border=0, bg='black')
        Suggestion.place(relx=0, rely=0, relheight=0.15, relwidth=1)

        back_tracking_widget = tk.Button(widget, font=('Georgia', 20), justify='center', fg='gray', text='⤽', activebackground='black', activeforeground='yellow', borderwidth=0, border=0, bg='black', command=previous_back_track_page_display)
        back_tracking_widget.place(relx=0, rely=0, relheight=0.005, relwidth=0.021)
        change_fg_OnHover(back_tracking_widget, 'yellow', 'gray')

        froward_tracking_widget = tk.Button(widget, font=('Georgia', 20), justify='center', fg='gray', text='⤼', activebackground='black', activeforeground='yellow', borderwidth=0, border=0, bg='black', command=previous_forwad_track_page_display)
        froward_tracking_widget.place(relx=0.021, rely=0, relheight=0.005, relwidth=0.021)
        change_fg_OnHover(froward_tracking_widget, 'yellow', 'gray')

        Search_box = tk.Entry(widget, font=('Georgia', 13), justify='center',   insertbackground="lightblue", borderwidth=0, border=0, bg='black', fg='gray')
        Search_box.place(relx=0.30, rely=0, relheight=0.007, relwidth=0.4)
        Search_box.insert(0, 'Search')
        Search_box.bind("<FocusIn>", lambda e: on_entry_click(Search_box, e))
        Search_box.bind("<FocusOut>", lambda e: on_focusout(Search_box, e))
        change_bg_OnHover(Search_box, '#010127', 'black')
        Search_box.bind("<Return>", lambda event: search_movies_request(top_frame_main, Search_box, event))

        # Section 2 ==================================================================================================================================================

        Suggestion1 = tk.Frame(Home_frame, borderwidth=0, border=0, bg='black')
        Suggestion1.place(relx=0, rely=0.151, relheight=0.17, relwidth=1)

        recomendation_tubs_bg_color = 'black'
        hover_color = 'lightblue'

        movies = imdb_other.popular_movies(genre=None, start_id=1, sort_by=None)  # returns top 50 popular movies starting from start id

        populer_movie_list = []
        for movie in movies['results']:
            movie_poster = clean_url(movie['poster'])
            populer_movie_list.append(( movie['name'], movie['year'], movie_poster, movie['id'].strip('t')))

        tk.Button(Suggestion1, font=('Georgia', 16), justify='center', anchor=tk.W, fg='gray', text='⍚ RECOMMENDED MOVIE', borderwidth=0, border=0, bg='black', command=lambda: Search_result(top_frame_main, populer_movie_list)).place(relx=0, rely=0, relheight=0.04, relwidth=1)

        PX_hight = int(Home_frame_hight * 0.17 * 0.31) - 1
        PY_width = int(screen_width * 1 * 0.12) - 1
        column = 0
        row = 0
        x_pos = 0.005
        y_pos = 0.05
        track = 0
        while row < 4: # 3
            while column < 8: # 8

                label1 = tk.Label(Suggestion1, bg=recomendation_tubs_bg_color, borderwidth=0, border=0)
                label1.place(relx=x_pos, rely=y_pos, relheight=0.31, relwidth=0.12)
                r1_bt1 = tk.Button(label1, bg='#1A2421', borderwidth=0, justify=tk.CENTER,  activebackground=hover_color, border=0, command=lambda id = populer_movie_list[track][3]: selected_movie_detail(id))
                r1_bt1.place(relx=0, rely=0, relwidth=1, relheight=1)
                # r1_img = imagen(populer_movie_list[track][2], PY_width, PX_hight)
                # r1_bt1.config(image=r1_img)
                # r1_bt1.image = r1_img
                change_bg_OnHover(r1_bt1, hover_color, '#1A2421')
                r1_bt2 = tk.Button(label1, borderwidth=0, border=0, bg=recomendation_tubs_bg_color, text=f'{populer_movie_list[track][0]}', activeforeground=hover_color, activebackground=recomendation_tubs_bg_color, fg='gray',  font=('Calibri', 11), command=lambda id=populer_movie_list[track]: selected_movie_detail(id))
                r1_bt2.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)
                change_fg_OnHover(r1_bt2, hover_color, 'gray')
                x_pos += 0.125
                column += 1
                track += 1

            column = 0
            x_pos = 0.005
            y_pos += 0.32
            row += 1

        # Section 3 ==========================================================================================================================================================

        Suggestion2 = tk.Frame(Home_frame, borderwidth=0, border=0, bg='black')
        Suggestion2.place(relx=0, rely=0.322, relheight=0.17, relwidth=1)

        series = imdb_other.popular_tv(genre=None, start_id=1, sort_by=None)  # returns top 50 popular TV Series starting from start id

        populer_series_list = []

        for TV in series['results']:
            TV_poster = clean_url(TV['poster'])
            populer_series_list.append(( TV['name'], TV['year'], TV_poster, TV['id'].strip('t')))

        tk.Button(Suggestion2, font=('Georgia', 16), justify='center', anchor=tk.W, fg='gray', text='⍚ RECOMMENDED SERIES', borderwidth=0, border=0, bg='black', command=lambda: Search_result(top_frame_main, populer_series_list)).place(relx=0, rely=0, relheight=0.04, relwidth=1)

        column = 0
        row = 0
        x_pos = 0.005
        y_pos = 0.05
        track = 0
        while row < 4:  # 3 rows
            while column < 8:  # 8 columns

                label3 = tk.Label(Suggestion2, bg=recomendation_tubs_bg_color, borderwidth=0, border=0)
                label3.place(relx=x_pos, rely=y_pos, relheight=0.31, relwidth=0.12)
                r1_bt3 = tk.Button(label3, bg='#1A2421', borderwidth=0, justify=tk.CENTER,  activebackground=hover_color, border=0, command=lambda id = populer_series_list[track][3]: selected_movie_detail(id))
                r1_bt3.place(relx=0, rely=0, relwidth=1, relheight=1)
                r3_img = imagen(populer_series_list[track][2], PY_width, PX_hight)
                r1_bt3.config(image=r3_img)
                r1_bt3.image = r3_img
                change_bg_OnHover(r1_bt3, hover_color, '#1A2421')
                r1_bt3 = tk.Button(label3, borderwidth=0, border=0, bg=recomendation_tubs_bg_color, text=f'{populer_series_list[track][0]}', activeforeground=hover_color, activebackground='#1A2421', fg='gray',  font=('Calibri', 11), command=lambda id= populer_movie_list[track]: selected_movie_detail(id))
                r1_bt3.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)

                change_fg_OnHover(r1_bt3, hover_color, 'gray')
                x_pos += 0.125
                column += 1
                track += 1

            column = 0
            x_pos = 0.005
            y_pos += 0.32
            row += 1


def main():
    global page_count, Home_frame
    global is_fullscreen
    global placeholder_text
    global screen_width
    global screen_height
    global large_frame_size, search_q, root
    global top_search_page, top_page, widget_track_position, top_frame_main, FRAME_1, FRAME_2, FRAME_1_canvas , canvas_FRAME_2

    if not have_runtime():  # 没有webview2 runtime
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
    search_q = tk.StringVar()

    FRAME_1 = tk.Frame(root, bg='yellow')
    FRAME_1.place(relx=0, rely=0, relwidth=1, relheight=1)
    FRAME_1_canvas = tk.Canvas(FRAME_1)
    FRAME_1_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    FRAME_1_scrollbar = tk.Scrollbar(root, command=FRAME_1_canvas.yview)
    FRAME_1_canvas.config(yscrollcommand=FRAME_1_scrollbar.set)
    FRAME_1_screen = tk.Frame(FRAME_1_canvas)
    FRAME_1_canvas.create_window((0, 0), window=FRAME_1_screen, anchor=tk.NW)
    widget_scroll_bind(FRAME_1_canvas)  # Bind the mouse wheel event to the canvas

    Home_frame_hight = screen_height * 5
    Home_frame = tk.Frame(FRAME_1_screen, bg='gray', width=screen_width, height=Home_frame_hight)
    Home_frame.pack(fill=tk.BOTH, expand=True)
    widget_track_position.append(Home_frame)
    page_count += 1


    FRAME_2 = tk.Frame(root)
    FRAME_2.place(relwidth=1, relheight=1, relx=0, rely=0)
    canvas_FRAME_2 = tk.Canvas(FRAME_2, highlightthickness=0) # Create a Canvas widget to hold the frame and enable scrolling
    canvas_FRAME_2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    canvas_FRAME_2_scrollbar = tk.Scrollbar(root, command=canvas_FRAME_2.yview) # Create a Scrollbar and connect it to the Canvas
    #canvas_FRAME_2_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas_FRAME_2.config(yscrollcommand=canvas_FRAME_2_scrollbar.set)
    canvas_FRAME_2_frame = tk.Frame(canvas_FRAME_2)     # Create a frame to hold your content of the canvers
    canvas_FRAME_2.create_window((0, 0), window=canvas_FRAME_2_frame, anchor=tk.NW)
    widget_scroll_bind(canvas_FRAME_2)  # Bind the mouse wheel event to the canvas

    main_frame = tk.Frame(canvas_FRAME_2_frame, bg='black', width=screen_width, height=large_frame_size)
    main_frame.pack(fill=tk.BOTH, expand=True)
    top_frame_main = main_frame



    Home_Page(Home_frame)


    root.mainloop()


if __name__ == "__main__":
    main()
    '''
    t = Thread(ThreadStart(main))
    t.ApartmentState = ApartmentState.STA
    t.Start()
    t.Join()
    '''


