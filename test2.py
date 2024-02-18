import requests


def get_new_movies (page = 1):
    r = requests.get('https://vidsrc.to/vapi/movie/new/1')  # latest movies
    print(r.status_code)
    movies = None
    length = 0
    if r.status_code == 200:
        data = r.json()
        length = data['result']['items']
        movies = data['result']['items']
    return movies, length


movies, count = get_new_movies()
print(movies)
print(movies[0]['imdb_id'])

