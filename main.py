import imdb

ia = imdb.Cinemagoer()
# Set up SQLite caching
print(dir(imdb))

movies = ia.search_movie('Spider-Man: Across the Spider-Verse')

print(movies)
print(type(movies))

# Fetch additional details, including images
ia.update(movies[0])
print("title", movies[0]['title'])
print("ID", movies[0].movieID)
print("Year:", movies[0]["year"])
print("Plot:", movies[0]["plot"])
print("Genres:", ", ".join(movies[0]["genres"]))
image_url = movies[0].get("full-size cover url", [])
print("Image URL:", image_url)
poster_urls = movies[0].get("cover url", [])
print("Image URL:", poster_urls)

print("Director:", ", ".join([director["name"] for director in movies[0]["director"]]))
print("Cast:", ", ".join([actor["name"] for actor in movies[0]["cast"]]))
print()
print(movies[0].current_info)



#for x in movies:
    # print(x)



# Search for people and companies

people = ia.search_person('angelina')
print(people[0]['name'])
print(people[0].personID)




companies = ia.search_company('rko')
print(companies[0]['name'])
print(companies[0].companyID)




