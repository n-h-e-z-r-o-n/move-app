import requests, time
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
    