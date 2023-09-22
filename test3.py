from PyMovieDb import IMDB
imdb = IMDB()
res = imdb.popular_movies(genre=None, start_id=1, sort_by=None)

print(res)