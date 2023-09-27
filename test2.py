
def on_entry_click(widget, event):
    print("on_entry_click :", widget.get())
    if widget.get() == "Search" or widget.get().isspace():
        widget.delete(0, tk.END)
        widget.config(fg='white')  # Change text color to black


def on_focusout(widget, event):
    print("on_focusout :", widget.get())
    if not widget.get() or widget.get().isspace():
        widget.delete(0, tk.END)
        widget.insert(0, "Search")
        widget.config(fg='gray')  # Change text color to gray

def search_movies_request(w, e, event):
    global search_q
    print("======>>> ", e.get())

def User_query_Pass(widget):
    print(widget.get)

import tkinter as tk


root = tk.Tk()

main_frame = tk.Frame(root, bg='black', width=1280, height=900)
main_frame.pack(fill=tk.X, expand=True)


Search_box = tk.Entry(main_frame,  font=('Georgia', 15), justify='center',  insertbackground="lightblue", borderwidth=0, border=0, bg='black', fg='white')
Search_box.place(relx=0.30, rely=0.007, relheight=0.017, relwidth=0.4)
Search_box.insert(0, 'Search')
Search_box.bind("<FocusIn>", lambda e: on_entry_click(Search_box, e))
Search_box.bind("<FocusOut>", lambda e: on_focusout(Search_box, e))
Search_box.bind("<Return>", lambda event: search_movies_request(root, Search_box, event))

Search_box2 = tk.Entry(main_frame, font=('Georgia', 15), justify='center',  insertbackground="lightblue", borderwidth=0, border=0, bg='BLUE', fg='white')
Search_box2.place(relx=0.30, rely=0.2, relheight=0.017, relwidth=0.4)


root.mainloop()