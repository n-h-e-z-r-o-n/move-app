import imdb
ia = imdb.Cinemagoer()
movies = ia.get_movie("1069185")
movie_poster_url = movies.get('full-size cover url')

print(movie_poster_url)
