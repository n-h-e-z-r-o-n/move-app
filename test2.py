from imdbmovies import IMDB
import imdb
from imdbmovies import IMDB
imdb_2 = IMDB()
ia = imdb.Cinemagoer()
movies = imdb_2.get_by_id("tt12593682")


print(movies['poster'])
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

def poster_image_get(movie_id):
    movies = imdb_2.get_by_id(movie_id)
    movie_poster_url = movies['poster']
    movie_poster_url = clean_url(movie_poster_url)
    """
    try:
        movies = ia.get_movie(movie_id[2:])
        movie_poster_url = movies.get('full-size cover url')
    except:
        movie_poster_url = None

    return  movie_poster_url
    """

    return movie_poster_url

m = poster_image_get("tt12593682")
print(m)