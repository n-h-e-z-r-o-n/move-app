from tkinter import *

root = Tk()
root.geometry("150x200")

w = Label(root, text ='GeeksForGeeks',
		font = "50")

w.pack()

scroll_bar = Scrollbar(root) 

scroll_bar.pack( side = RIGHT,
				fill = Y )

mylist = Listbox(root,
				yscrollcommand = scroll_bar.set )

for line in range(1, 26):
	mylist.insert(END, "Geeks " + str(line))

mylist.pack( side = LEFT, fill = BOTH )

scroll_bar.config( command = mylist.yview )

root.mainloop()



"""
from imdb import Cinemagoer

# create an instance of the Cinemagoer class
ia = Cinemagoer()

# get a movie
movie = ia.get_movie('31381010')


genres = ','.join(i for i in movie['genres'])



print(movie.data)



print(genres)


print(movie['cover url'])
print(movie['imdbID'])
print(movie['kind'])
print(movie['year'])
print(movie['title'])

print(movie['plot'][0])
"""