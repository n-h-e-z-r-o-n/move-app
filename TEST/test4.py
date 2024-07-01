import tmdbsimple as tmdb
tmdb.API_KEY = 'af9b2e27c1a6bc3233af1832f4acc850'
#tmdb.REQUESTS_SESSION = requests.Session()
movie = tmdb.Movies(603)
response = movie.info()
print(movie.title)
'The Matrix'
print(movie.budget)

