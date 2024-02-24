from imdbmovies import IMDB
imdb_other = IMDB()


movies = imdb_other.get_by_id("tt30750708")
movie_poster_url = movies['poster']
print(movie_poster_url)