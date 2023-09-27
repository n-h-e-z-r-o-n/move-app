import imdb

ia = imdb.Cinemagoer()
# Set up SQLite caching



movies = ia.search_movie('The originals')



# Fetch additional details, including images
ia.update(movies[0])
print(movies[0].infoset2keys)
print("kind", movies[0]['kind'])
print("year", movies[0]['year'])


#print("number of seasons:", movies[0]['number of seasons'])
#print("seasons", movies[0]['seasons'])
print("production companies", movies[0]['production companies'])

print("countries", movies[0]['countries'])
print("rating", movies[0]['rating'])
print("cover url", movies[0]['cover url'])

print("akas", movies[0]['akas'])
print("languages", movies[0]['languages'])
print("title", movies[0]['title'])
print("original title", movies[0]['original title'])
print("ID", movies[0].movieID)
print("Year:", movies[0]["year"])
print("Plot:", movies[0]["plot"])
print("Genres:", movies[0]["genres"])
print("Cast:", ", ".join([actor["name"] for actor in movies[0]["cast"]]))



def writers():
    i = 0
    writers_str = ''
    while i < len(movies[0]["writer"]):
        if len( movies[0]["writer"][i]) != 0:
            writers_str += str(movies[0]["writer"][i]) + '. '

        i += 1

    return writers_str

def cast():
    i = 0
    cast_str = ''
    while i < len(movies[0]["cast"]):
        if len( movies[0]["cast"][i]) != 0:
            cast_str += str(movies[0]["cast"][i]) + '. '

        i += 1

    return cast_str
print("Cast:", cast())

print("writer", writers())


def genres():
    i = 0
    genres_str = ''
    for  i in movies[0]["genres"]:
        genres_str += str(i) + ', '


    return genres_str


genres_n = genres()
print("genres", genres_n)


def production():
    i = 0
    production_str = ''
    while i < len(movies[0]['production companies']) :
        if len(movies[0]['production companies'][i]) != 0 and i < 5:
            production_str += str(movies[0]['production companies'][i]) + ', '
        i += 1
    return production_str

production_str = production()
print("production_str", production_str)

poster_url = movies[0].get('full-size cover url')
print("Poster URL:", poster_url)

m = ia.get_popular100_movies()
print(m)
m = ia.get_popular100_tv()
#print(m)

# print("Director:", ", ".join([director["name"] for director in movies[0]["director"]]))
# print("Cast:", ", ".join([actor["name"] for actor in movies[0]["cast"]]))
# print()
# print(movies[0].current_info)



#for x in movies:
    # print(x)


'''
# Search for people and companies

people = ia.search_person('angelina')
print(people[0]['name'])
print(people[0].personID)




companies = ia.search_company('rko')
print(companies[0]['name'])
print(companies[0].companyID
)
'''




