import requests
def get_new_tv_shows (page = 1):
    r = requests.get(f'https://vidsrc.to/vapi/tv/new/{page}')  # latest movies
    print(r.status_code)
    movies = None
    length = 0
    if r.status_code == 200:
        data = r.json()
        length = len(data['result']['items'])
        movies = data['result']['items']
    return movies, length

movies, length = get_new_tv_shows()

print(movies[0]['name'])