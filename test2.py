from PyMovieDb import IMDB
imdb = IMDB()
res = imdb.popular_movies(genre=None, start_id=1, sort_by=None)
# returns top 50 popular movies starting from start id
print(res)
print(type(res))


import json
# Opening JSON file
f = open('m.json',)
# returns JSON object as
# a dictionary
data = json.load(f)
# Iterating through the json
# list
for i in data['results']:
    print(i['id'])
# Closing file
f.close()
