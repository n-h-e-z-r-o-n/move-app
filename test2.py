from imdbmovies import IMDB

def Selected(movie)
imdb_other = IMDB()
movies = imdb_other.get_by_id("tt0944947")
print(movies)
movie_name = movies['name']
movie_type = movies['type']
movie_genre = movies['genre']
movie_datePublished = movies['datePublished']
movie_ratingValue = movies['rating']['ratingValue']
movie_poster_url = movies['poster']
movie_actor = movies['actor']
movie_description = movies['description']


print(movie_actor)


