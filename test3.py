import imdb

# Create an instance of the IMDb class
ia = imdb.IMDb()

# Search for a movie by its title
movie_title = "The Shawshank Redemption"
movies = ia.search_movie(movie_title)

if movies:
    # Get the first movie (most relevant)
    movie = movies[0]

    # Fetch additional details, including images
    ia.update(movie)

    # Print the movie's details
    print("Title:", movie["title"])
    print("Year:", movie["year"])
    print("Plot:", movie["plot"])
    print("Genres:", ", ".join(movie["genres"]))

    # Access the movie's images

image_url = movie.get("full-size cover url", [])
print("Image URL:", image_url)

