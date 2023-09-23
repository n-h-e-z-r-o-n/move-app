import imdb

ia = imdb.Cinemagoer()
movies = ia.search_movie('Avengers')
ia.update(movies[0])  # Fetch additional details, including images


def cast():
    i = 0
    cast_str = ''
    while i < len(movies[0]["cast"]):
        if len(movies[0]["cast"][i]) != 0 and i < 15:
            cast_str += str(movies[0]["cast"][i]) + ', '
        i += 1

    return cast_str


def production():
    i = 0
    production_str = ''
    while i < len(movies[0]['production companies']):
        if len(movies[0]['production companies'][i]) != 0 and i < 5:
            production_str += str(movies[0]['production companies'][i]) + ', '
        i += 1
    return production_str


def genres():
    genres_str = ''
    for i in movies[0]["genres"]:
        genres_str += str(i) + ', '
    return genres_str


def country():
    country_str = ''
    for i in movies[0]["countries"]:
        country_str += str(i) + '. '
    return country_str


def plot():
    plot_str = ''
    for i in movies[0]["plot"]:
        plot_str += str(i)
    return plot_str


movie_id = movies[0].movieID
movie_title = movies[0]['title']
movie_ratting = movies[0]['rating']
movie_type = movies[0]['kind']
movie_country = country()
movie_genres = genres()
movie_year = movies[0]['year']
movie_production_company = production()
movie_cast_names = cast()
movie_plot = plot()

# (widget, movie_id, movie_title, movie_ratting, movie_type, movie_country, movie_genres, movie_year, movie_production_company, movie_cast_names, movie_plot, movie_poster_url)
movie_poster_url = movies[0].get('full-size cover url')