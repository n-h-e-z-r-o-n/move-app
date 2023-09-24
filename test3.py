import imdb
# 13622776
# 4154796
# creating instance of IMDb
ia = imdb.Cinemagoer()

# id
code = "13622776"

# getting information
series = ia.get_movie(code)

episode_ids = ia.get_movie_episodes(series, 1)

# getting seasons of the series
season = series.data['seasons']

# printing the object i.e name
print(series['series years'])
print(series['number of seasons'])
print(series['seasons'])

# print the seasons
print(series.infoset2keys)
# adding new info set
