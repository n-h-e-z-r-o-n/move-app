# (title, year, post_url, movie_id)
import requests
r = requests.get(f'https://vidsrc.to/vapi/movie/add/{page}')  # latest movies
movies = None
length = 0
if r.status_code == 200:
    data = r.json()
    length = len(data['result']['items'])
    movies = data['result']['items']

print(movies)