import imdb
ia = imdb.Cinemagoer()
movies = ia.get_movie(25406412)
movie_poster_url = movies.get('full-size cover url')

print(movie_poster_url)
