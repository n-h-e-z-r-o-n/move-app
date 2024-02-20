import imdb
ia = imdb.IMDb()

print(dir(ia))
M = ia.search_keyword('action')

print(M)
