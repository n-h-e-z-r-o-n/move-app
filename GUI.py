# ================= libraries imports ==============================================================================================================
# =====================================================================================================================================================
import colorsys
import tkinter as tk
from PIL import Image, ImageTk

from io import BytesIO

import random
import time
import threading

from imdbmovies import IMDB
import imdb
import requests
import ctypes as ct  # used for dark mode
import io
import base64

# =================================================  integrating pywebview  ===========================================================================
# =====================================================================================================================================================
import ctypes
from webview.window import Window
from webview.platforms.edgechromium import EdgeChrome
from tkinter import Frame
from System.Windows.Forms import Control
from System.Threading import Thread, ApartmentState, ThreadStart, SynchronizationContext, SendOrPostCallback

user32 = ctypes.windll.user32


class WebView2(Frame):
    def __init__(self, parent, width: int, height: int, url: str = '', **kw):
        Frame.__init__(self, parent, width=width, height=height, **kw)
        control = Control()
        uid = 'master'
        window = Window(uid, str(id(self)), url=None, html=None, js_api=None, width=width, height=height, x=None, y=None,
                        resizable=True, fullscreen=False, min_size=(200, 100), hidden=False,
                        frameless=False, easy_drag=True,
                        minimized=False, on_top=False, confirm_close=False, background_color='#FFFFFF',
                        transparent=False, text_select=True, localization=None,
                        zoomable=True, draggable=True, vibrancy=False)
        self.window = window
        self.web_view = EdgeChrome(control, window, None)
        self.control = control
        self.web = self.web_view.web_view
        self.width = width
        self.height = height
        self.parent = parent
        self.chwnd = int(str(self.control.Handle))
        user32.SetParent(self.chwnd, self.winfo_id())
        user32.MoveWindow(self.chwnd, 0, 0, width, height, True)
        self.loaded = window.events.loaded
        self.__go_bind()
        if url != '':
            self.load_url(url)
        self.core = None

    def __go_bind(self):
        self.bind('<Destroy>', lambda event: self.web.Dispose())
        self.bind('<Configure>', self.__resize_webview)
        self.newwindow = None

    def __resize_webview(self, event):
        user32.MoveWindow(self.chwnd, 0, 0, self.winfo_width(), self.winfo_height(), True)

    def load_url(self, url):
        self.web_view.load_url(url)


# ================= Global Variables Definition =======================================================================================================
# =====================================================================================================================================================

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

ia = imdb.Cinemagoer()

imdb_other = IMDB()


# ================= Functions Definition ==============================================================================================================
# =====================================================================================================================================================

def dark_title_bar(window):  # dark mode navegation bar
    window.update()
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ct.windll.user32.GetParent
    hwnd = get_parent(window.winfo_id())
    rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
    value = 1
    value = ct.c_int(value)
    set_window_attribute(hwnd, rendering_policy, ct.byref(value), ct.sizeof(value))


def clean_url(url):
    url = url
    url = url.replace('_V1_', '_V1000_')  # Replace '_V1_' with '_V1000_'
    url = url.replace('_UX67_', '_UX1000_')  # Replace '_UX67_' with '_UX1000_'
    url = url.replace('_UY98_', '_UY1000_')
    url = url.replace('_SX101_', '_SX1000_')
    url = url.replace('_CR0,0,101,150_', '_CR0,0,0,0_')
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
    def xxx(widget=widget, increment=None):
        current_scroll = float(widget.yview()[0])
        new_scroll = max(0.0, min(1.0, current_scroll + increment))
        widget.yview_moveto(new_scroll)

    # Scroll the canvas up or down based on the mouse wheel direction
    if event.delta < 0:
        # widget.yview_scroll(1, "units")
        xxx(widget, 0.01)

        # widget.update_idletasks()  # Force update of the display

    else:
        # widget.yview_scroll(-1, "units")
        xxx(widget, -0.01)
        # widget.update_idletasks()  # Force update of the display


prevy = 0


def on_touch_scroll(widget, event):
    global prevy

    def xxx(widget=widget, increment=None):
        current_scroll = float(widget.yview()[0])
        new_scroll = max(0.0, min(1.0, current_scroll + increment))
        widget.yview_moveto(new_scroll)

    nowy = event.y_root

    if nowy > prevy:
        xxx(widget, -0.004)
        # widget.yview_scroll(-1, "units")
    elif nowy < prevy:
        xxx(widget, 0.004)
        # widget.yview_scroll(1, "units")

    else:
        event.delta = 0
    prevy = nowy
    widget.unbind_all("<Button-1>"), "+"


def widget_scroll_bind(widget):
    widget.bind("<Configure>", lambda e: on_frame_configure(widget, e))
    widget.bind_all("<MouseWheel>", lambda e: on_mouse_wheel(widget, e))
    widget.bind_all("<B1-Motion>", lambda e: on_touch_scroll(widget, e))
    widget.bind("<Leave>", lambda _: widget.unbind_all("<B1>"))


def imagen(image_url, screen_width, screen_height, widget):
    def load_image():
        retry = 0
        while retry < 6:
            try:
                if image_url is None:
                    image = Image.open("./Default.png")
                else:
                    response = requests.get(image_url, timeout=20)
                    image_data = response.content
                    image = Image.open(BytesIO(image_data))

                image = image.resize((screen_width, screen_height), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                widget.config(image=photo)
                widget.image = photo  # Keep a reference to the PhotoImage to prevent it from being garbage collected
                retry = 7  # End  while looop
            except:
                retry += 1
                time.sleep(5)

    image_thread = threading.Thread(target=load_image)  # Create a thread to load the image asynchronously
    image_thread.start()


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

    image_thread = threading.Thread(target=load_image)  # Create a thread to load the image asynchronously
    image_thread.start()


def poster_image_get(movie_id):
    try:
        movies = imdb_other.get_by_id(movie_id)
        movie_poster_url = movies['poster']
        movie_poster_url = clean_url(movie_poster_url)
    except:
        movie_poster_url = None
    """
    try:
        movies = ia.get_movie(movie_id[2:])
        movie_poster_url = movies.get('full-size cover url')
    except:
        movie_poster_url = None

    return  movie_poster_url
    """
    return movie_poster_url


def imagen_fade(movie_id, screen_height, screen_width, widget):
    def load_img_url(widget=widget, movie_id=movie_id):
        poster_url = poster_image_get(movie_id)
        retry = 0
        while retry < 6:
            try:
                if poster_url is None:
                    image = (Image.open("./Default.png"))
                else:
                    # Download the image from the web
                    response = requests.get(poster_url)
                    image_data = response.content
                    image = Image.open(BytesIO(image_data))  # Create a PIL Image object from the image data

                # Resize the image to match the frame's dimensions
                h = screen_height  # - 200
                image = image.resize((screen_width, (h)), Image.LANCZOS)
                # Ensure the image has an alpha channel.
                im = image.convert("RGBA")
                try:
                    width, height = im.size
                except:
                    continue
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

                photo = ImageTk.PhotoImage(im)
                widget.config(image=photo, compound=tk.CENTER)
                widget.image = photo  # Keep a reference to the PhotoImage to prevent it from being garbage collected
                retry = 7
            except:
                retry += 1
                time.sleep(5)

    threading.Thread(target=load_img_url).start()  # Create a thread


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


def rrr(movie_id):
    global top_frame_main

    # watch_page(top_frame_main, movie_id, movie_title, movie_ratting, movie_type, movie_country, movie_genres, movie_year, movie_production_company, movie_cast_names, movie_plot, movie_poster_url, r1_title, r1_year, recomednation_1_poster, r2_title, r2_year, recomednation_2_poster, r3_title, r3_year, recomednation_3_poster, r4_title, r4_year, recomednation_4_poster, r5_title, r5_year, recomednation_5_poster, r6_title, r6_year, recomednation_6_poster, r1_id, r2_id, r3_id, r4_id, r5_id, r6_id)


def selected_movie_detail(movie_id):
    movies = imdb_other.get_by_id(movie_id)
    movie_name = movies['name']
    movie_type = movies['type']
    movie_genre = ", ".join(i for i in movies['genre'])
    movie_datePublished = movies['datePublished']
    movie_ratingValue = movies['rating']['ratingValue']
    movie_poster_url = movies['poster']
    movie_actor = ", ".join(i['name'] for i in movies['actor'])
    movie_description = movies['description']
    movie_country = None
    movie_production_company = None

    # return movie_name, movie_type, movie_genre, movie_datePublished, movie_ratingValue, movie_poster_url, movie_actor, movie_description
    watch_page(top_frame_main, movie_id, movie_name, movie_ratingValue, movie_type, movie_country, movie_genre, movie_datePublished, movie_production_company, movie_actor, movie_description, movie_poster_url)


def watch_page(widget, movie_id, movie_title, movie_ratting, movie_type, movie_country, movie_genres, movie_year, movie_production_company, movie_cast_names, movie_plot, movie_poster_url):
    global screen_width
    global screen_height
    global large_frame_size
    global top_frame_main
    global widget_track_position, search_q
    global page_count, FRAME_1, FRAME_2, canvas_FRAME_2, FRAME_1_canvas

    FRAME_2.tkraise()
    widget_scroll_bind(canvas_FRAME_2)

    i_high = int(large_frame_size * 0.2) - 4
    i_widh = int(screen_width * 0.15) - 4
    pi_high = int(large_frame_size * 0.16)
    pi_widh = int(screen_width * 0.13)

    # Create a large frame within the canvas frame (replace this with your content)
    large_frame = tk.Frame(widget, bg='black', width=screen_width, height=large_frame_size)
    large_frame.place(relwidth=1, relheight=1, relx=0, rely=0)
    widget_track_position.append(large_frame)
    large_frame.tkraise()
    page_count += 1

    label3 = tk.Label(large_frame, bg='black')
    label3.place(relx=0.04, rely=0.52, relheight=0.16, relwidth=0.13)
    imagen(movie_poster_url, pi_widh, pi_high, label3)

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

    # Add = tk.Text(large_frame, bg='green', fg='gray', borderwidth=0, border=0, wrap=tk.WORD, font=('Comic Sans MS', 12))
    # Add.place(relx=0.04, rely=0.727, relheight=0.037, relwidth=0.95)

    #  content:
    image_label = tk.Button(large_frame, text='▷', bg='black', fg='white', borderwidth=0, border=0, activebackground='black', activeforeground='yellow', relief=tk.FLAT, font=('Arial Black', 76, 'bold'), command=lambda: play(video_box))
    image_label.place(relx=0, rely=0.0, relheight=0.5, relwidth=1)
    imagen_fade(movie_id, screen_height, screen_width, image_label)
    change_fg_OnHover(image_label, 'yellow', 'white')

    back_tracking_widget = tk.Button(large_frame, font=('Georgia', 20), justify='center', fg='gray', text='⤽', activebackground='black', activeforeground='yellow', borderwidth=0, border=0, bg='black', command=previous_back_track_page_display)
    back_tracking_widget.place(relx=0, rely=0, relheight=0.017, relwidth=0.021)
    change_fg_OnHover(back_tracking_widget, 'yellow', 'gray')

    froward_tracking_widget = tk.Button(large_frame, font=('Georgia', 20), justify='center', fg='gray', text='⤼', activebackground='black', activeforeground='yellow', borderwidth=0, border=0, bg='black', command=previous_forwad_track_page_display)
    froward_tracking_widget.place(relx=0.021, rely=0, relheight=0.017, relwidth=0.021)
    change_fg_OnHover(froward_tracking_widget, 'yellow', 'gray')

    reload = tk.Button(large_frame, font=('Georgia', 20), justify='center', fg='gray', text='⥁', activebackground='black', activeforeground='yellow', borderwidth=0, border=0, bg='black', command=lambda: frame2.reload())
    reload.place(relx=0.042, rely=0, relheight=0.017, relwidth=0.021)

    Search_box = tk.Entry(large_frame, font=('Georgia', 15), justify='center', insertbackground="lightblue", borderwidth=0, border=0, bg='black', fg='white')
    Search_box.place(relx=0.30, rely=0, relheight=0.017, relwidth=0.4)
    Search_box.insert(0, 'Search')
    Search_box.bind("<FocusIn>", lambda e: on_entry_click(Search_box, e))
    Search_box.bind("<FocusOut>", lambda e: on_focusout(Search_box, e))
    change_bg_OnHover(Search_box, '#010127', 'black')
    Search_box.bind("<Return>", lambda event: search_movies_request(top_frame_main, Search_box, large_frame, 0, event))

    recomendation_tubs_bg_color = '#1A2421'
    hover_color = 'lightblue'
    text_color = 'gray'

    recomedation_other = []
    label2 = tk.Frame(large_frame, bg=recomendation_tubs_bg_color, borderwidth=0, border=0)
    label2.place(relx=0.04, rely=0.78, relheight=0.2, relwidth=0.15)
    r1_bt1 = tk.Button(label2, bg=recomendation_tubs_bg_color, borderwidth=0, activebackground=hover_color, font=('Calibri', 11, 'bold'), border=0)
    r1_bt1.place(relx=0, rely=0, relwidth=1, relheight=1)
    # imagen(recomednation_1_poster, i_widh, i_high, r1_bt1)
    change_bg_OnHover(r1_bt1, hover_color, recomendation_tubs_bg_color)
    r1_bt2 = tk.Button(label2, borderwidth=0, border=0, bg='black', activeforeground=hover_color, activebackground=recomendation_tubs_bg_color, font=('Calibri', 11, 'bold'), fg=text_color)
    r1_bt2.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)
    change_fg_OnHover(r1_bt2, hover_color, text_color)
    recomedation_other.append((r1_bt1, r1_bt2))

    label3 = tk.Frame(large_frame, bg=recomendation_tubs_bg_color, borderwidth=0, border=0)
    label3.place(relx=0.2, rely=0.78, relheight=0.2, relwidth=0.15)
    r2_bt1 = tk.Button(label3, bg=recomendation_tubs_bg_color, activebackground=hover_color, borderwidth=0, border=0)
    r2_bt1.place(relx=0, rely=0, relwidth=1, relheight=1)
    # imagen(recomednation_2_poster, i_widh, i_high, r2_bt1)
    change_bg_OnHover(r2_bt1, hover_color, recomendation_tubs_bg_color)
    r2_bt2 = tk.Button(label3, borderwidth=0, border=0, bg='black', activeforeground=hover_color, activebackground=recomendation_tubs_bg_color, font=('Calibri', 11, 'bold'), fg=text_color)
    r2_bt2.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)
    change_fg_OnHover(r2_bt2, hover_color, text_color)
    recomedation_other.append((r2_bt1, r2_bt2))

    label4 = tk.Frame(large_frame, bg=recomendation_tubs_bg_color, borderwidth=0, border=0)
    label4.place(relx=0.36, rely=0.78, relheight=0.2, relwidth=0.15)
    r3_bt1 = tk.Button(label4, bg=recomendation_tubs_bg_color, activebackground=hover_color, borderwidth=0, border=0)
    r3_bt1.place(relx=0, rely=0, relwidth=1, relheight=1)
    # imagen(recomednation_3_poster, i_widh, i_high, r3_bt1)
    change_bg_OnHover(r3_bt1, hover_color, recomendation_tubs_bg_color)
    r3_bt2 = tk.Button(label4, borderwidth=0, border=0, bg='black', activeforeground=hover_color, activebackground=recomendation_tubs_bg_color, font=('Calibri', 11, 'bold'), fg=text_color)
    r3_bt2.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)
    change_fg_OnHover(r3_bt2, hover_color, text_color)
    recomedation_other.append((r3_bt1, r3_bt2))

    label5 = tk.Frame(large_frame, bg=recomendation_tubs_bg_color, borderwidth=0, border=0)
    label5.place(relx=0.52, rely=0.78, relheight=0.2, relwidth=0.15)
    r4_bt1 = tk.Button(label5, bg=recomendation_tubs_bg_color, activebackground=hover_color, borderwidth=0, border=0)
    r4_bt1.place(relx=0, rely=0, relwidth=1, relheight=1)
    # imagen(recomednation_4_poster, i_widh, i_high, r4_bt1)
    change_bg_OnHover(r4_bt1, hover_color, recomendation_tubs_bg_color)
    r4_bt2 = tk.Button(label5, borderwidth=0, border=0, bg='black', activeforeground=hover_color, activebackground=recomendation_tubs_bg_color, font=('Calibri', 11, 'bold'), fg=text_color)
    r4_bt2.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)
    change_fg_OnHover(r4_bt2, hover_color, text_color)
    recomedation_other.append((r4_bt1, r4_bt2))

    label6 = tk.Frame(large_frame, bg=recomendation_tubs_bg_color, borderwidth=0, border=0)
    label6.place(relx=0.68, rely=0.78, relheight=0.2, relwidth=0.15)
    r5_bt1 = tk.Button(label6, bg=recomendation_tubs_bg_color, activebackground=hover_color, borderwidth=0, border=0)
    r5_bt1.place(relx=0, rely=0, relwidth=1, relheight=1)
    # imagen(recomednation_5_poster, i_widh, i_high, r5_bt1)
    change_bg_OnHover(r5_bt1, hover_color, recomendation_tubs_bg_color)
    r5_bt2 = tk.Button(label6, borderwidth=0, border=0, bg='black', activeforeground=hover_color, activebackground=recomendation_tubs_bg_color, font=('Calibri', 11, 'bold'), fg=text_color)
    r5_bt2.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)
    change_fg_OnHover(r5_bt2, hover_color, text_color)
    recomedation_other.append((r5_bt1, r5_bt2))

    label7 = tk.Frame(large_frame, bg=recomendation_tubs_bg_color, borderwidth=0, border=0)
    label7.place(relx=0.84, rely=0.78, relheight=0.2, relwidth=0.15)
    r6_bt1 = tk.Button(label7, bg=recomendation_tubs_bg_color, activebackground=hover_color, borderwidth=0, border=0)
    r6_bt1.place(relx=0, rely=0, relwidth=1, relheight=1)
    # imagen(recomednation_6_poster, i_widh, i_high, r6_bt1)
    change_bg_OnHover(r6_bt1, hover_color, recomendation_tubs_bg_color)
    r6_bt2 = tk.Button(label7, borderwidth=0, border=0, bg='black', activeforeground=hover_color, activebackground=recomendation_tubs_bg_color, font=('Calibri', 11, 'bold'), fg=text_color)
    r6_bt2.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)
    change_fg_OnHover(r6_bt2, hover_color, text_color)
    recomedation_other.append((r6_bt1, r6_bt2))

    video_box = tk.Frame(large_frame, bg='black')
    frame2 = WebView2(video_box, 500, 500)
    frame2.load_url(f'https://vidsrc.to/embed/tv/tt0944947')  # https://vidsrc.to/embed/movie/tt{movie_id}
    frame2.place(relheight=1, relwidth=1, relx=0, rely=0)
    video_box.bind("<Double-Button-1>", print("double clicked"))

    if random.randint(0, 1):
        threading.Thread(target=recommendation_movies, args=(recomedation_other, i_widh, i_high)).start()
    else:
        threading.Thread(target=recommendation_tv, args=(recomedation_other, i_widh, i_high)).start()


def Animation(wid):
    # Load the animated GIF using Pillow
    gif = Image.open("search_animation.gif")
    frames = []
    frame_index = 0
    # Split the GIF into frames
    try:
        while True:
            frame = gif.copy()
            frames.append(ImageTk.PhotoImage(frame))
            gif.seek(len(frames))
    except EOFError:
        pass

    def update_image(index):
        try:
            if wid.winfo_exists():
                frame = frames[index]
                wid.config(image=frame)
                index = (index + 1) % len(frames)
                root.after(100, lambda c=index: update_image(c))  # Change the delay (in milliseconds) to control the animation speed
        except Exception as e:
            # print(f"Error updating image: {e}")
            return

    update_image(frame_index)


def search_movies_request(widget, user_query, wig_tp, i, event):
    load_animation = tk.Label(wig_tp, bg='black', border=0, borderwidth=0)
    if i == 1:
        load_animation.place(relx=0.70, rely=0, relheight=0.007, relwidth=0.07)
    else:
        load_animation.place(relx=0.70, rely=0, relheight=0.017, relwidth=0.07)
    Animation(load_animation)

    def retrieving_movie_data():
        user_search_query = user_query.get()
        search_results = ia.search_movie(user_search_query)
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

        load_animation.destroy()
        Search_result(widget, movie_list)

    image_thread = threading.Thread(target=retrieving_movie_data)  # Create a thread to load the image asynchronously
    image_thread.start()


def previous_back_track_page_display():
    global page_count, widget_track_position, FRAME_1, FRAME_2, FRAME_1_canvas, canvas_FRAME_2
    if page_count > 0:
        page_count -= 1
        if page_count == 0:
            FRAME_1.tkraise()
            widget_scroll_bind(FRAME_1_canvas)
        else:
            FRAME_2.tkraise()
            widget_scroll_bind(canvas_FRAME_2)

        widget_track_position[page_count].tkraise()


def previous_forwad_track_page_display():
    global page_count, widget_track_position, FRAME_1, FRAME_2, FRAME_1_canvas, canvas_FRAME_2
    if page_count < (len(widget_track_position) - 1):
        page_count += 1
        if page_count == 0:
            FRAME_1.tkraise()
            widget_scroll_bind(FRAME_1_canvas)
        else:
            FRAME_2.tkraise()
            widget_scroll_bind(canvas_FRAME_2)
        widget_track_position[page_count].tkraise()


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
    Search_box.place(relx=0.30, rely=0.007, relheight=0.02, relwidth=0.4)
    Search_box.insert(0, "Search")
    Search_box.bind("<FocusIn>", lambda e: on_entry_click(Search_box, e))
    Search_box.bind("<FocusOut>", lambda e: on_focusout(Search_box, e))
    change_bg_OnHover(Search_box, '#010127', 'black')
    Search_box.bind("<Return>", lambda event: search_movies_request(top_frame_main, Search_box, widget, 0, event))

    recomendation_tubs_bg_color = 'black'
    hover_color = 'lightblue'

    def grid(widget, movies_list_result, total_movies, track):
        for i in movie_list_grid:
            i.destroy()
        i_high = int(large_frame_size * 0.2) - 4
        i_widh = int(screen_width * 0.15) - 4
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
                label1 = tk.Frame(widget, bg=recomendation_tubs_bg_color, borderwidth=0, border=0)
                label1.place(relx=x_pos, rely=y_pos, relheight=0.2, relwidth=0.15)
                r1_bt1 = tk.Button(label1, bg='#1A2421', borderwidth=0, activebackground=hover_color, border=0, command=lambda id=movies_list_result[track][3]: selected_movie_detail(id))
                r1_bt1.place(relx=0, rely=0, relwidth=1, relheight=1)
                imagen(movies_list_result[track][2], i_widh, i_high, r1_bt1)
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

        if (total_movies - track) > 0:
            pages = tk.Button(Search_result_frame, bg=recomendation_tubs_bg_color, font=('Colonna MT', 15, 'bold'), activebackground=recomendation_tubs_bg_color,
                              activeforeground='green', text="next", fg='gray', justify=tk.CENTER, borderwidth=0, border=0)
            pages.config(command=lambda a=Search_result_frame, b=movies_list_result, c=total_movies, d=track: grid(a, b, c, d))
            pages.place(rely=0.91, relx=0.4, relheight=0.02, relwidth=0.09)
            movie_list_grid.append(pages)
            change_fg_OnHover(pages, 'lightblue', 'gray')

        if track > 24:
            track = track - (current_widgets + 24)
            pages1 = tk.Button(Search_result_frame, bg=recomendation_tubs_bg_color, font=('Colonna MT', 15, 'bold'), activebackground=recomendation_tubs_bg_color,
                               activeforeground='green', text="previous", fg='gray', justify=tk.CENTER, borderwidth=0, border=0)
            pages1.config(command=lambda a=Search_result_frame, b=movies_list_result, c=total_movies, d=track: grid(a, b, c, d))
            pages1.place(rely=0.91, relx=0.5, relheight=0.02, relwidth=0.09)
            movie_list_grid.append(pages1)
            change_fg_OnHover(pages1, 'lightblue', 'gray')

    grid(Search_result_frame, m_list, len(m_list), 0)


# ------------------------------- Movie fetch function -------- -----------------------------------------------
def get_new_movies(page=1):
    r = requests.get(f'https://vidsrc.to/vapi/movie/new/{page}')  # latest movies
    print(r.status_code)
    movies = None
    length = 0
    if r.status_code == 200:
        data = r.json()
        length = len(data['result']['items'])
        movies = data['result']['items']
    return movies, length


def get_added_movies(page=1):
    r = requests.get(f'https://vidsrc.to/vapi/movie/add/{page}')  # latest movies
    movies = None
    length = 0
    if r.status_code == 200:
        data = r.json()
        length = len(data['result']['items'])
        movies = data['result']['items']
    return movies, length


def get_new_tv_shows(page=1):
    r = requests.get(f'https://vidsrc.to/vapi/tv/new/{page}')  # latest movies
    movies = None
    length = 0
    if r.status_code == 200:
        data = r.json()
        length = len(data['result']['items'])
        movies = data['result']['items']
    return movies, length


def get_added_tv_shows(page=1):
    r = requests.get(f'https://vidsrc.to/vapi/tv/add/{page}')  # latest movies
    movies = None
    length = 0
    if r.status_code == 200:
        data = r.json()
        length = len(data['result']['items'])
        movies = data['result']['items']
    return movies, length


def populer_new_tv_shows(widget_list, PX_hight, PY_width):
    tv_shows_list = []
    movies, x = get_new_tv_shows(1)
    tv_shows_list.extend(movies)
    movies, x = get_new_tv_shows(2)
    tv_shows_list.extend(movies)
    count = 0
    for widget in widget_list:
        widget[1].config(text=tv_shows_list[count]["title"])
        imagen(poster_image_get(tv_shows_list[count]["imdb_id"]), PY_width, PX_hight, widget[0])
        widget[0].config(command=lambda id=tv_shows_list[count]["imdb_id"]: selected_movie_detail(id))
        widget[1].config(command=lambda id=tv_shows_list[count]["imdb_id"]: selected_movie_detail(id))
        count += 1


def populer_added_tv_shows(widget_list, PX_hight, PY_width):
    tv_shows_list = []
    movies, x = get_added_tv_shows(1)
    tv_shows_list.extend(movies)
    movies, x = get_added_tv_shows(2)
    tv_shows_list.extend(movies)
    count = 0
    for widget in widget_list:
        widget[1].config(text=tv_shows_list[count]["title"])
        imagen(poster_image_get(tv_shows_list[count]["imdb_id"]), PY_width, PX_hight, widget[0])
        widget[0].config(command=lambda id=tv_shows_list[count]["imdb_id"]: selected_movie_detail(id))
        widget[1].config(command=lambda id=tv_shows_list[count]["imdb_id"]: selected_movie_detail(id))
        count += 1


def populer_new_moves(widget_list, PX_hight, PY_width):
    movie_list = []
    movies, x = get_new_movies(1)
    movie_list.extend(movies)
    movies, x = get_new_movies(2)
    movie_list.extend(movies)
    print("p movies", len(movie_list))
    count = 0
    for widget in widget_list:
        widget[1].config(text=movie_list[count]["title"])
        imagen(poster_image_get(movie_list[count]["imdb_id"]), PY_width, PX_hight, widget[0])
        widget[0].config(command=lambda id=movie_list[count]["imdb_id"]: selected_movie_detail(id))
        widget[1].config(command=lambda id=movie_list[count]["imdb_id"]: selected_movie_detail(id))
        count += 1


def populer_added_moves(widget_list, PX_hight, PY_width):
    movie_list = []
    movies, x = get_added_movies(1)
    movie_list.extend(movies)
    movies, x = get_added_movies(2)
    movie_list.extend(movies)
    print("p movies", len(movie_list))
    count = 0
    for widget in widget_list:
        widget[1].config(text=movie_list[count]["title"])
        imagen(poster_image_get(movie_list[count]["imdb_id"]), PY_width, PX_hight, widget[0])
        widget[0].config(command=lambda id=movie_list[count]["imdb_id"]: selected_movie_detail(id))
        widget[1].config(command=lambda id=movie_list[count]["imdb_id"]: selected_movie_detail(id))
        count += 1


def recommendation_movies(widget_list, PY_width, PX_hight):
    page = random.randint(1, 100)
    movies, x = get_new_movies(page)
    count = 0
    for widget in widget_list:
        widget[1].config(text=movies[count]["title"])
        imagen(poster_image_get(movies[count]["imdb_id"]), PY_width, PX_hight, widget[0])
        widget[0].config(command=lambda id=movies[count]["imdb_id"]: selected_movie_detail(id))
        widget[1].config(command=lambda id=movies[count]["imdb_id"]: selected_movie_detail(id))
        count += 1


def recommendation_tv(widget_list, PY_width, PX_hight):
    page = random.randint(1, 100)
    tvs, x = get_new_tv_shows(page)
    count = 0
    for widget in widget_list:
        widget[1].config(text=tvs[count]["title"])
        imagen(poster_image_get(tvs[count]["imdb_id"]), PY_width, PX_hight, widget[0])
        widget[0].config(command=lambda id=tvs[count]["imdb_id"]: selected_movie_detail(id))
        widget[1].config(command=lambda id=tvs[count]["imdb_id"]: selected_movie_detail(id))
        count += 1


def Fetch_Mount(numer=24):
    global New_moves, Added_moves, New_TV_Shows, Added_TV_Shows

    def xr(shows_list):
        for movie in shows_list:
            movie_id = movie['imdb_id']
            title = movie['title']
            year = ''
            poster =  poster_image_get(movie_id)

            movie_list.append((title, year, poster, movie_id))  # (title, year, post_url, movie_id)

    new_movie_list = []
    added_movie_list = []
    new_tvs_list = []
    added_tvs_list = []
    count = 0
    while count < numer:
        movies_new, len1 = get_new_movies(page=count)
        movies_added, len2 = get_added_movies(page=count)
        tv_new, len3 = get_new_tv_shows(page=count)
        tv_added, len3 = get_added_tv_shows(page=count)

        new_movie_list.extend(movies_new)
        added_movie_list.extend(movies_added)
        new_tvs_list.extend(tv_new)
        added_tvs_list.extend(tv_added)

        count += 1




    return movie_list


# ---------------------------------------------------------------------------------------------------------------

def slide_show(widget):
    global screen_height, screen_width, root

    def Home_page_Background_changer(list, x=0):
        if len(list) == 0:
            return
        global root
        list = list
        if x == 4:
            list[x].tkraise()
            x = 1
        elif x == 3:
            list[x].tkraise()
            x += 1
        elif x == 2:
            list[x].tkraise()
            x += 1
        elif x == 1:
            list[x].tkraise()
            x += 1
        else:
            list[x].tkraise()
            x += 1
        root.after(7000, lambda: Home_page_Background_changer(list, x=x))

    movies, num = get_new_movies(2)
    list = []
    if num != 0:
        count = 0
        for movie in movies:
            if count > 4:
                break
            f1 = tk.Button(widget, borderwidth=0, border=0, text=movie['title'], fg='white', activebackground='black', bg='black')  # , command=lambda id=movie[count]['imdb_id']: selected_movie_detail(id))
            f1.place(relx=0, rely=0, relheight=1, relwidth=1)
            imagen_fade(movie['imdb_id'], screen_height, screen_width, f1)
            count += 1
            list.append(f1)

        Home_page_Background_changer(list)


def Home_Page(widget):
    global widget_track_position, page_count, screen_height, screen_width, canvas_FRAME_2, FRAME_1_canvas, top_frame_main, Home_frame

    FRAME_1.tkraise()
    widget_scroll_bind(FRAME_1_canvas)
    Home_frame_hight = screen_height * 5
    PX_hight = int(Home_frame_hight * 0.17 * 0.31) - 1
    PY_width = int(screen_width * 1 * 0.12) - 1
    # background image ======================================================================
    Home_label = tk.Label(widget, bg='gray')
    Home_label.place(relx=0, rely=0, relwidth=1, relheight=1)
    bg_sections = 'black'

    # ===========  Section 1  =========================================================================================================================================

    Suggestion = tk.Frame(widget, borderwidth=0, border=0, bg=bg_sections)
    Suggestion.place(relx=0, rely=0, relheight=0.15, relwidth=1)

    back_tracking_widget = tk.Button(widget, font=('Georgia', 20), justify='center', fg='gray', text='⤽', activebackground='black', activeforeground='yellow', borderwidth=0, border=0, bg='black', command=previous_back_track_page_display)
    back_tracking_widget.place(relx=0, rely=0, relheight=0.005, relwidth=0.021)
    change_fg_OnHover(back_tracking_widget, 'yellow', 'gray')

    froward_tracking_widget = tk.Button(widget, font=('Georgia', 20), justify='center', fg='gray', text='⤼', activebackground='black', activeforeground='yellow', borderwidth=0, border=0, bg='black', command=previous_forwad_track_page_display)
    froward_tracking_widget.place(relx=0.021, rely=0, relheight=0.005, relwidth=0.021)
    change_fg_OnHover(froward_tracking_widget, 'yellow', 'gray')

    Search_box = tk.Entry(widget, font=('Georgia', 13), justify='center', insertbackground="lightblue", borderwidth=0, border=0, bg='black', fg='gray')
    Search_box.place(relx=0.30, rely=0, relheight=0.007, relwidth=0.4)
    Search_box.insert(0, 'Search')
    Search_box.bind("<FocusIn>", lambda e: on_entry_click(Search_box, e))
    Search_box.bind("<FocusOut>", lambda e: on_focusout(Search_box, e))
    change_bg_OnHover(Search_box, '#010127', 'black')
    Search_box.bind("<Return>", lambda event: search_movies_request(top_frame_main, Search_box, widget, 1, event))

    # ===========  Section 2  =========================================================================================================================================

    section2 = tk.Frame(widget, borderwidth=0, border=0, bg=bg_sections)
    section2.place(relx=0, rely=0.151, relheight=0.17, relwidth=1)
    recomendation_tubs_bg_color = 'black'
    hover_color = 'lightblue'

    p_ms2 = tk.Button(section2, font=('Georgia', 16), justify='center', anchor=tk.W, activeforeground='lightblue', fg='gray', text=' ⍚ NEW MOVIES', borderwidth=0, border=0, bg='black')  # , command=lambda: Search_result(top_frame_main, populer_movie_list))
    p_ms2.place(relx=0, rely=0, relheight=0.04, relwidth=1)
    change_fg_OnHover(p_ms2, 'lightblue', 'gray')

    column = 0
    row = 0
    x_pos = 0.005
    y_pos = 0.05
    track = 0
    movies_new_widget = []
    while row < 3:  # 3
        while column < 8:  # 8

            label1 = tk.Frame(section2, bg=recomendation_tubs_bg_color, borderwidth=0, border=0)
            label1.place(relx=x_pos, rely=y_pos, relheight=0.31, relwidth=0.12)
            r1_bt1 = tk.Button(label1, bg='#1A2421', borderwidth=0, justify=tk.CENTER, activebackground=hover_color, border=0)
            r1_bt1.place(relx=0, rely=0, relwidth=1, relheight=1)
            change_bg_OnHover(r1_bt1, hover_color, '#1A2421')
            r1_bt2 = tk.Button(label1, borderwidth=0, border=0, bg=recomendation_tubs_bg_color, activeforeground=hover_color, activebackground=recomendation_tubs_bg_color, fg='gray', font=('Calibri', 11))
            r1_bt2.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)
            change_fg_OnHover(r1_bt2, hover_color, 'gray')
            movies_new_widget.append((r1_bt1, r1_bt2))
            x_pos += 0.125
            column += 1
            track += 1

        column = 0
        x_pos = 0.005
        y_pos += 0.32
        row += 1

    # ===========  Section 3  =========================================================================================================================================

    section3 = tk.Frame(widget, borderwidth=0, border=0, bg=bg_sections)
    section3.place(relx=0, rely=0.322, relheight=0.17, relwidth=1)

    p_ms3 = tk.Button(section3, font=('Georgia', 16), justify='center', anchor=tk.W, fg='gray', activeforeground='lightblue', text=' ⍚ RECENT MOVIES', borderwidth=0, border=0, bg='black')  # , command=lambda: Search_result(top_frame_main, populer_series_list))
    p_ms3.place(relx=0, rely=0, relheight=0.04, relwidth=1)
    change_fg_OnHover(p_ms3, 'lightblue', 'gray')

    column = 0
    row = 0
    x_pos = 0.005
    y_pos = 0.05
    track = 0
    movies_added_widget = []
    while row < 3:  # 3 rows
        while column < 8:  # 8 columns
            label3 = tk.Frame(section3, bg=recomendation_tubs_bg_color, borderwidth=0, border=0)
            label3.place(relx=x_pos, rely=y_pos, relheight=0.31, relwidth=0.12)
            r1_bt3 = tk.Button(label3, bg='#1A2421', borderwidth=0, justify=tk.CENTER, activebackground=hover_color, border=0)
            r1_bt3.place(relx=0, rely=0, relwidth=1, relheight=1)
            change_bg_OnHover(r1_bt3, hover_color, '#1A2421')
            r1_bt4 = tk.Button(label3, borderwidth=0, border=0, bg=recomendation_tubs_bg_color, text='', activeforeground=hover_color, activebackground='#1A2421', fg='gray', font=('Calibri', 11))
            r1_bt4.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)
            movies_added_widget.append((r1_bt3, r1_bt4))
            change_fg_OnHover(r1_bt4, hover_color, 'gray')
            x_pos += 0.125
            column += 1
            track += 1

        column = 0
        x_pos = 0.005
        y_pos += 0.32
        row += 1

    # ===========  Section 4  =========================================================================================================================================

    section4 = tk.Frame(widget, borderwidth=0, border=0, bg=bg_sections)
    section4.place(relx=0, rely=0.493, relheight=0.17, relwidth=1)

    p_ms4 = tk.Button(section4, font=('Georgia', 16), justify='center', anchor=tk.W, activeforeground='lightblue', fg='gray', text=' ⍚ NEW SERIES', borderwidth=0, border=0, bg='black')  # , command=lambda: Search_result(top_frame_main, populer_movie_list))
    p_ms4.place(relx=0, rely=0, relheight=0.04, relwidth=1)
    change_fg_OnHover(p_ms4, 'lightblue', 'gray')

    column = 0
    row = 0
    x_pos = 0.005
    y_pos = 0.05
    track = 0
    tvs_new_widgets = []
    while row < 3:  # 3 rows
        while column < 8:  # 8 columns
            label3 = tk.Frame(section4, bg=recomendation_tubs_bg_color, borderwidth=0, border=0)
            label3.place(relx=x_pos, rely=y_pos, relheight=0.31, relwidth=0.12)
            r1_bt3 = tk.Button(label3, bg='#1A2421', borderwidth=0, justify=tk.CENTER, activebackground=hover_color, border=0)  # , command=lambda id = populer_series_list[track][3]: selected_movie_detail(id))
            r1_bt3.place(relx=0, rely=0, relwidth=1, relheight=1)
            change_bg_OnHover(r1_bt3, hover_color, '#1A2421')
            r1_bt4 = tk.Button(label3, borderwidth=0, border=0, bg=recomendation_tubs_bg_color, text='', activeforeground=hover_color, activebackground='#1A2421', fg='gray', font=('Calibri', 11))  # , command=lambda id= populer_movie_list[track]: selected_movie_detail(id))
            r1_bt4.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)
            tvs_new_widgets.append((r1_bt3, r1_bt4))
            change_fg_OnHover(r1_bt4, hover_color, 'gray')
            x_pos += 0.125
            column += 1
            track += 1

        column = 0
        x_pos = 0.005
        y_pos += 0.32
        row += 1

    # ===========  Section 5  =========================================================================================================================================

    section5 = tk.Frame(widget, borderwidth=0, border=0, bg=bg_sections)
    section5.place(relx=0, rely=0.664, relheight=0.17, relwidth=1)

    p_ms5 = tk.Button(section5, font=('Georgia', 16), justify='center', anchor=tk.W, activeforeground='lightblue', fg='gray', text=' ⍚ ADDED SERIES', borderwidth=0, border=0, bg='black')  # , command=lambda: Search_result(top_frame_main, populer_movie_list))
    p_ms5.place(relx=0, rely=0, relheight=0.04, relwidth=1)
    change_fg_OnHover(p_ms5, 'lightblue', 'gray')

    column = 0
    row = 0
    x_pos = 0.005
    y_pos = 0.05
    track = 0
    tvs_added_widget = []
    while row < 3:  # 3 rows
        while column < 8:  # 8 columns
            label3 = tk.Frame(section5, bg=recomendation_tubs_bg_color, borderwidth=0, border=0)
            label3.place(relx=x_pos, rely=y_pos, relheight=0.31, relwidth=0.12)
            r1_bt3 = tk.Button(label3, bg='#1A2421', borderwidth=0, justify=tk.CENTER, activebackground=hover_color, border=0)  # , command=lambda id = populer_series_list[track][3]: selected_movie_detail(id))
            r1_bt3.place(relx=0, rely=0, relwidth=1, relheight=1)
            change_bg_OnHover(r1_bt3, hover_color, '#1A2421')
            r1_bt4 = tk.Button(label3, borderwidth=0, border=0, bg=recomendation_tubs_bg_color, text='', activeforeground=hover_color, activebackground='#1A2421', fg='gray', font=('Calibri', 11))  # , command=lambda id= populer_movie_list[track]: selected_movie_detail(id))
            r1_bt4.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)
            tvs_added_widget.append((r1_bt3, r1_bt4))
            change_fg_OnHover(r1_bt4, hover_color, 'gray')
            x_pos += 0.125
            column += 1
            track += 1

        column = 0
        x_pos = 0.005
        y_pos += 0.32
        row += 1

    # imagen_2("Assets/12.jpg", screen_width, Home_frame_hight, Home_label)
    threading.Thread(target=slide_show, args=(Suggestion,)).start()
    threading.Thread(target=populer_new_moves, args=(movies_new_widget, PX_hight, PY_width)).start()
    threading.Thread(target=populer_added_moves, args=(movies_added_widget, PX_hight, PY_width)).start()
    threading.Thread(target=populer_new_tv_shows, args=(tvs_new_widgets, PX_hight, PY_width)).start()
    threading.Thread(target=populer_added_tv_shows, args=(tvs_added_widget, PX_hight, PY_width)).start()


# ================= Main Definition ===================================================================================================================
# =====================================================================================================================================================
def Start_graphics():
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
    m = tk.Label(root)
    m.pack(fill='both', expand=True)

    imagen_2("Assets/startup.jpg", start_w, start_h, m)

    C.overrideredirect(True)
    C.config(bg='blue')

    def on_closing():
        C.destroy()

    m.after(5000, on_closing)
    C.mainloop()


def main():
    global page_count, Home_frame
    global is_fullscreen
    global placeholder_text, root
    global screen_width
    global screen_height
    global large_frame_size, search_q, root
    global top_search_page, top_page, widget_track_position, top_frame_main, FRAME_1, FRAME_2, FRAME_1_canvas, canvas_FRAME_2

    root = tk.Tk()
    root.title("Move App")
    root.state('zoomed')  # this creates a window that takes over the screen
    root.minsize(500, 600)
    root.attributes("-topmost", True)

    dark_title_bar(root)

    # Get the screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    large_frame_size = screen_height + 700
    search_q = tk.StringVar()
    Home_frame_hight = screen_height * 5

    FRAME_1 = tk.Frame(root, )
    FRAME_1.place(relx=0, rely=0, relwidth=1, relheight=1)
    FRAME_1_canvas = tk.Canvas(FRAME_1, borderwidth=0, highlightthickness=0)
    FRAME_1_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    FRAME_1_scrollbar = tk.Scrollbar(root, command=FRAME_1_canvas.yview)
    FRAME_1_canvas.config(yscrollcommand=FRAME_1_scrollbar.set)
    FRAME_1_screen = tk.Frame(FRAME_1_canvas, bg='')
    FRAME_1_canvas.create_window((0, 0), window=FRAME_1_screen, anchor=tk.NW)
    widget_scroll_bind(FRAME_1_canvas)  # Bind the mouse wheel event to the canvas

    Home_frame = tk.Frame(FRAME_1_screen, bg='', width=screen_width, height=Home_frame_hight)
    Home_frame.pack(fill=tk.BOTH, expand=True)

    widget_track_position.append(Home_frame)
    page_count += 1

    FRAME_2 = tk.Frame(root, bg='black')
    FRAME_2.place(relwidth=1, relheight=1, relx=0, rely=0)
    canvas_FRAME_2 = tk.Canvas(FRAME_2, borderwidth=0, highlightthickness=0)  # Create a Canvas widget to hold the frame and enable scrolling
    canvas_FRAME_2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    canvas_FRAME_2_scrollbar = tk.Scrollbar(root, command=canvas_FRAME_2.yview)  # Create a Scrollbar and connect it to the Canvas
    canvas_FRAME_2.config(yscrollcommand=canvas_FRAME_2_scrollbar.set)
    canvas_FRAME_2_frame = tk.Frame(canvas_FRAME_2)  # Create a frame to hold your content of the canvers
    canvas_FRAME_2.create_window((0, 0), window=canvas_FRAME_2_frame, anchor=tk.NW)
    widget_scroll_bind(canvas_FRAME_2)  # Bind the mouse wheel event to the canvas

    main_frame = tk.Frame(canvas_FRAME_2_frame, bg='black', width=screen_width, height=large_frame_size)
    main_frame.pack(fill=tk.BOTH, expand=True)
    top_frame_main = main_frame

    root.attributes("-topmost", False)

    Home_Page(Home_frame)
    # selected_movie_detail("tt0944947")
    # watch_page(main_frame, '10638522', 'Talk to Me', 7.2, 'movie', 'Australia. United Kingdom. ', 'Horror, Thriller, ', 2022, 'Causeway Films, Head Gear Films, Metrol Technology, Screen Australia, Talk to Me Holdings, ', 'Ari McCarthy, Hamish Phillips, Kit Erhart-Bruce, Sarah Brokensha, Jayden Davison, Sunny Johnson, Sophie Wilde, Marcus Johnson, Kidaan Zelleke, James Oliver, Joe Bird, Jett Gazley, Alexandra Jensen, Dog, Helene Philippou', 'ghg' ,'eet')
    root.mainloop()


if __name__ == "__main__":
    # Start_graphics()
    main()
    """
    t = Thread(ThreadStart(main))
    t.ApartmentState = ApartmentState.STA
    t.Start()
    t.Join()
    """
