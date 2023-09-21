import imdb

# Create an IMDbPY instance
ia = imdb.IMDb()

# Search for a movie by its title
movie_title = "AHSOKA"  # Replace with the title of the movie you're interested in
search_results = ia.search_movie(movie_title)

# Check if search results are available and get the first result
if search_results:
    movie_id = search_results[0].getID()
    movie = ia.get_movie(movie_id)

    # Get the release date of the movie
    release_date = movie.get("month")

    print("Release Date:", release_date)

