from imdb import Cinemagoer

# create an instance of the Cinemagoer class
ia = Cinemagoer()

# get a movie
movie = ia.get_movie('31381010')


genres = ','.join(i for i in movie['genres'])



print(genres)

print(movie['number of seasons'])
print(movie['rating'])
print(movie['cover url'])
print(movie['imdbID'])
print(movie['kind'])
print(movie['year'])
print(movie['title'])

print(movie['plot'][0])
