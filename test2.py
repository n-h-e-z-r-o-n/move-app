from imdbmovies import IMDB

#def Selected(movie_id):
imdb_other = IMDB()
movies = imdb_other.get_by_id("tt0944947")
movie_name = movies['name']
movie_type = movies['type']
movie_genre = movies['genre']
movie_datePublished = movies['datePublished']
movie_ratingValue = movies['rating']['ratingValue']
movie_poster_url = movies['poster']
movie_actor = "".join(i for i in movies['actor']['name'])
movie_description = movies['description']

#return movie_name, movie_type, movie_genre, movie_datePublished, movie_ratingValue, movie_poster_url, movie_actor, movie_description

print(movie_actor)

