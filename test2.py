import requests
start_run_time_time = time.time()
r = requests.get('https://vidsrc.to/vapi/movie/new/1') # latest movies
print(r.status_code)
if  r.status_code == 200:
    data = r.json()
    print(len(data['result'][ 'items']))
    print(data['result'][ 'items'])
end = time.time()

print(start_run_time_time-end)

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

