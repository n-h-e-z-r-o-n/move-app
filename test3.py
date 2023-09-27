
# 13622776
# 4154796
import imdb
from imdbmovies import IMDB
imdb_other = IMDB()
ia = imdb.Cinemagoer()


# res = imdb.upcoming(region=None)

# print(res)

# res = imdb_other.popular_movies(genre=None, start_id=1, sort_by=None) # returns top 50 popular movies starting from start id

res = imdb_other.popular_tv(genre=None, start_id=1, sort_by=None) # returns top 50 popular TV Series starting from start id

print(res)
print(res['results'][0])
def clean(url):
    movie_poster = url
    movie_poster = movie_poster.replace('_V1_', '_V1000_')  # Replace '_V1_' with '_V1000_'
    movie_poster = movie_poster.replace('_UX67_', '_UX1000_')  # Replace '_UX67_' with '_UX1000_'
    movie_poster = movie_poster.replace('_UY98_', '_UY1000_')
    movie_poster = movie_poster.replace('_CR0,0,67,98_', '_CR0,0,0,0_')  # Replace '_CR0,0,67,98_' with '_CR0,0,0,0_'
    movie_poster = movie_poster.replace('_CR5,0,67,98_', '_CR0,0,0,0_')  # Replace '_CR5,0,67,98_' with '_CR0,0,0,0_'
    movie_poster = movie_poster.replace('_CR1,0,67,98_', '_CR0,0,0,0_')  # Replace '_CR1,0,67,98_' with '_CR0,0,0,0_'

    return movie_poster

for i in res['results']:

    print(i['id'])
    print(i['name'])
    print(i['year'])
    # print(clean(i['poster']), '\n')
    print(i['poster'], '\n')



# print(res)
