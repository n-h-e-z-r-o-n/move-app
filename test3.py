# (title, year, post_url, movie_id)
import requests
def get_added_movies(page=1):
    r = requests.get(f'https://vidsrc.to/vapi/movie/add/{1}')  # latest movies
    movies = None
    length = 0
    if r.status_code == 200:
        data = r.json()
        length = len(data['result']['items'])
        movies = data['result']['items']

    for movie in movies:
        movie_id = movie['imdb_id']
        title = movie['title']
        year = ''

print(movies)