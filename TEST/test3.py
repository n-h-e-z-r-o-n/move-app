import requests


r = requests.get(f'https://api.themoviedb.org/3/discover/tv?&api_key=6bfaa39b0a3a25275c765dcaddc7dae7&page=1')  # latest movies
if r.status_code == 200:
    data = r.json()
    print(len(data['results']))

print(data['results'][0])
for i in data['results'][0]:
    print(i )

