import imdb

ia = imdb.Cinemagoer()

movies = ia.search_movie('matrix')

print(movies)
print(type(movies))


print(movies[0]['title'])
print(movies[0].movieID)

#for x in movies:
    # print(x)



# Search for people and companies

people = ia.search_person('angelina')
print(people[0]['name'])
print(people[0].personID)




companies = ia.search_company('rko')
print(companies[0]['name'])
print(companies[0].companyID)




