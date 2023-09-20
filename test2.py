from tkinter import * 

cnt=1
def msgShow():
    global cnt
    # label["text"] = "I love Python x" + str(cnt)
    # label["bg"] = "lightyellow"
    # label["fg"] = "blue"
    label.config(text="I love Python x" + str(cnt),
            bg="lightyellow",fg="blue")
    cnt += 1

root = Tk()
root.title("apidemos.com")
root.geometry("300x300")
label = Label(root)
# label["text"] = "I love Java"

btn = Button(root,command=msgShow,
                cursor="star")
label.pack()
btn.pack()

root.mainloop()