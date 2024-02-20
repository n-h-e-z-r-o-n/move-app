import imdb
ia = imdb.IMDb()

print(dir(ia))
M = ia.search_movie('Avengers')

print(M)
