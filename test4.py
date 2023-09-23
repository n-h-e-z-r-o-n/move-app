import imdb
movie_list = []
#ia = imdb.Cinemagoer()
ia = imdb.IMDb()
search_results = ia.search_movie("The Originals")
print(search_results[0])

print(search_results[0].movieID)

year = ia.get_movie(1452938).data['movie year']



print(year)

