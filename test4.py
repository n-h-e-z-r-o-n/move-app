import requests
def get_new_movies (page = 1):
    r = requests.get(f'https://vidsrc.to/vapi/movie/new/{page}')  # latest movies
    print(r.status_code)
    movies = None
    length = 0
    if r.status_code == 200:
        data = r.json()
        length = data['result']['items']
        movies = data['result']['items']
    return movies, length




def get_added_movies (page = 1):
    r = requests.get(f'https://vidsrc.to/vapi/movie/add/{page}')  # latest movies
    print(r.status_code)
    movies = None
    length = 0
    if r.status_code == 200:
        data = r.json()
        length = data['result']['items']
        movies = data['result']['items']
    return movies, length






def get_new_tv_shows (page = 1):
    r = requests.get(f'https://vidsrc.to/vapi/tv/new/{page}')  # latest movies
    print(r.status_code)
    movies = None
    length = 0
    if r.status_code == 200:
        data = r.json()
        length = data['result']['items']
        movies = data['result']['items']
    return movies, length


def get_added_tv_shows (page = 1):
    r = requests.get(f'https://vidsrc.to/vapi/tv/add/{page}')  # latest movies
    print(r.status_code)
    movies = None
    length = 0
    if r.status_code == 200:
        data = r.json()
        length = data['result']['items']
        movies = data['result']['items']
    return movies, length

def get_added_episode(page = 1):
    r = requests.get(f'https://vidsrc.to/vapi/episode/latest/{page}')  # latest movies
    print(r.status_code)
    movies = None
    length = 0
    if r.status_code == 200:
        data = r.json()
        length = data['result']['items']
        movies = data['result']['items']
    return movies, length


m, l  = get_added_episode(page = 1)

print(m)