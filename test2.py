import imdb
ia = imdb.Cinemagoer()

print(dir(ia))
M = ia.get_top50_tv_by_genres('Action')
print(M)
