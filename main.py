import imdb
ia = imdb.Cinemagoer()
m='tt22488984'
movies = ia.get_movie(m[2:])
movie_poster_url = movies.get('full-size cover url')

print(movie_poster_url)

def