import imdb
ia = imdb.IMDb()

print(dir(ia))
M = ia.search_keyword('avengers')
M = ia.search_person()
print(M)
