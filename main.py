import imdb
ia = imdb.Cinemagoer()
m='tt25406412'
movies = ia.get_movie(m[2:])
movie_poster_url = movies.get('full-size cover url')

print(dir(movies))
