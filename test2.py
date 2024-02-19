import requests


def get_new_movies (page = 1):
    movies = []

    while page < 5:
        r = requests.get(f'https://vidsrc.to/vapi/movie/new/{page}')  # latest movies
        print(r.status_code)
        if r.status_code == 200:
            data = r.json()
            movies.extend(data['result']['items'])
        page += 1
    return movies, len(movies)

movies, count = get_new_movies()
print(movies)
print(count)

