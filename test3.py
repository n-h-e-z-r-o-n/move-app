# (title, year, post_url, movie_id)
import requests
def (page=1):

    movie_list = []
    for movie in movies:
        movie_id = movie['imdb_id']
        title = movie['title']
        year = ''
        poster = '' #poster_image_get(movie_id)
        movie_list.append((title, year, poster, movie_id))  # (title, year, post_url, movie_id)

    return movie_list

print(movies)