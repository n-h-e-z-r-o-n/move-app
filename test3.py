import imdb
movie_list = []
#ia = imdb.Cinemagoer()
ia = imdb.IMDb()
search_results = ia.search_movie("The Originals")
print(search_results)



# 1452938

for movie in search_results:
    title = movie['title']
    print(title)
    movie_id = movie.movieID
    try:
       year = movie['year']
    except:

        try:
           year = ia.get_movie(movie_id).data['series years']
        except:
            year = ''

    post_url = movie.get('full-size cover url')
    movie_list.append((title, year, post_url, movie_id))

print(movie_list)