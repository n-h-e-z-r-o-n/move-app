import imdb

ia = imdb.Cinemagoer()

movies = ia.search_movie('matrix')

print(movies)
print(type(movies))

# Fetch additional details, including images
ia.update(movies[0])
print("title", movies[0]['title'])
print("ID", movies[0].movieID)
print("Year:", movies[0]["year"])
print("Plot:", movies[0]["plot"])

#for x in movies:
    # print(x)



# Search for people and companies

people = ia.search_person('angelina')
print(people[0]['name'])
print(people[0].personID)




companies = ia.search_company('rko')
print(companies[0]['name'])
print(companies[0].companyID)




