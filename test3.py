from imdbmovies import IMDB
imdb = IMDB()
res = imdb.upcoming(region=None)
# returns upcomming movies info as json