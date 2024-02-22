import requests

# Making a GET request
r = requests.get('https://www.imdb.com/title/tt1190634/episodes/?ref_=tt_eps_sm')

# check status code for response received
# success code - 200
print(r)

# print content of request
print(r.content)