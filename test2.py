#Import the required libraries
from tkinter import *

#Create an instance of Tkinter Frame
win = Tk()

#Set the geometry
win.geometry("700x350")

#Adding transparent background property
win.wm_attributes('-transparentcolor', '#ab23ff')

#Create a Label
Label(win, text= "Hello World!", font= ('Helvetica 18'), bg= '#ab23ff').pack(ipadx= 50, ipady=50, padx= 20)

win.mainloop()
