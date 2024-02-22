import requests
url = 'https://www.imdb.com/title/tt1190634/episodes?season=1'


r = requests.get(url)  # latest movies
print(r)
data = r.json()
length = len(data['result']['items'])
movies = data['result']['items']

print(movies)