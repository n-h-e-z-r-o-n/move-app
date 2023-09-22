import tkinter as tk
import clr
from tkwebview2.tkwebview2 import WebView2, have_runtime, install_runtime
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Threading')
from System.Windows.Forms import Control
from System.Threading import Thread,ApartmentState,ThreadStart

def on_double_click(event):
  print("yes")
def main():
    if not have_runtime():#没有webview2 runtime
        install_runtime()
    root=tk.Tk()
    root.title('pywebview for tkinter test')
    root.geometry('1200x600+5+5')


    p = tk.Frame(root)
    p.place(relheight=1,relwidth=1,rely=0,relx=0)
    frame2 = WebView2(p,500,500)
    frame2.pack(side='left',padx=0,fill='both',expand=True)
    frame2.load_url('https://vidsrc.to/embed/movie/tt4154796')

    # Bind the double-click event to the frame
    p.bind("<Double-Button-1>", on_double_click)
    frame2.bind("<Double-Button-1>", on_double_click)
    root.mainloop()

if __name__ == "__main__":
    t = Thread(ThreadStart(main))
    t.ApartmentState = ApartmentState.STA
    t.Start()
    t.Join()