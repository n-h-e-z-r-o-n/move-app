import time
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

i = 0
import threading
from imdbmovies import IMDB
imdb_other = IMDB()

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

def imagen_fade(poster_url, screen_height, screen_width, widget):
    def load_img_url(widget=widget):
        retry = 0
        while retry < 6:
            try:
                if poster_url is None:
                    image = (Image.open("./Default.png"))
                else:
                    # Download the image from the web
                    response = requests.get(poster_url, timeout=20)
                    image_data = response.content
                    image = Image.open(BytesIO(image_data))  # Create a PIL Image object from the image data

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

                photo = ImageTk.PhotoImage(im)
                widget.config(image=photo, compound=tk.CENTER)
                widget.image = photo  # Keep a reference to the PhotoImage to prevent it from being garbage collected
                retry = 7

            except requests.exceptions.RequestException as e:
                print(f"Error loading image Fade: {e}")
                retry += 1
                time.sleep(5)
    image_thread = threading.Thread(target=load_img_url)  # Create a thread
    image_thread.start()

def Home_page_Background_changer(list, x = 0):
    list = list
    if x == 4:
        print(x)
        list[x].tkraise()
        x = 1
    elif x == 3:
        print(x)
        list[x].tkraise()
        x += 1
    elif x == 2:
        print(x)
        list[x].tkraise()
        x += 1
    elif x == 1:
        print(x)
        list[x].tkraise()
        x += 1
    else:
        print(x)
        list[x].tkraise()
        x += 1
    root.after(4000, lambda : Home_page_Background_changer(list, x = x))

def slide_show(widget):
    global screen_height, screen_width
    print(screen_width, ' = = ', screen_height)

    movies = imdb_other.popular_movies(genre=None, start_id=1, sort_by=None)  # returns top 50 popular movies starting from start id

    show_movie_list = []
    for movie in movies['results']:
        movie_poster = clean_url(movie['poster'])
        show_movie_list.append((movie['name'], movie['year'], movie_poster, movie['id'].strip('t')))

    print(show_movie_list)
    f1 = tk.Button(widget,  borderwidth=0, border=0, bg='black')
    f1.place(relx=0, rely=0, relheight=1, relwidth=1)
    imagen_fade(show_movie_list[9][2], screen_height, screen_width, f1)

    f2 = tk.Button(widget,  borderwidth=0, border=0, bg='black')
    f2.place(relx=0, rely=0, relheight=1, relwidth=1)
    imagen_fade(show_movie_list[12][2], screen_height, screen_width, f2)

    f3 = tk.Button(widget,  borderwidth=0, border=0, bg='black')
    f3.place(relx=0, rely=0, relheight=1, relwidth=1)
    imagen_fade(show_movie_list[15][2], screen_height, screen_width, f3)

    f4 = tk.Button(widget,  borderwidth=0, border=0, bg='black')
    f4.place(relx=0, rely=0, relheight=1, relwidth=1)
    imagen_fade(show_movie_list[24][2], screen_height, screen_width, f4)

    f5 = tk.Button(widget,  borderwidth=0, border=0, bg='black')
    f5.place(relx=0, rely=0, relheight=1, relwidth=1)
    imagen_fade(show_movie_list[7][2], screen_height, screen_width, f5)

    list = [f1, f2, f3, f4, f5]

    Home_page_Background_changer(list)

screen_height = 1280
screen_width = 1920
root = tk.Tk()
root.geometry("400x200")

Suggestion = tk.Frame(root,  borderwidth=0, border=0, bg='black')
Suggestion.place(relx=0, rely=0, relheight=0.5, relwidth=1)
#imagen_fade('https://m.media-amazon.com/images/M/MV5BYmI4MzE2YjQtYWMxYi00MjBhLThhOTYtYjdiOGQ4NzE4MWViXkEyXkFqcGdeQXVyMzUwNDIxMjQ@._V1000_UY1000_CR0,0,0,0_AL_.jpg', screen_height, screen_width, Suggestion)


slide_show(Suggestion)


root.mainloop()
