import threading
import webview
from tkinter import Frame,Tk,Button
import ctypes


from webview.window import Window
from webview.platforms.edgechromium import EdgeChrome

from System.Windows.Forms import Control
from System.Threading import Thread,ApartmentState,ThreadStart,SynchronizationContext,SendOrPostCallback

user32=ctypes.windll.user32


class WebView2(Frame):
    def __init__(self,parent,width:int,height:int,url:str='',**kw):
        Frame.__init__(self,parent,width=width,height=height,**kw)
        control=Control()
        uid = 'master'
        window=Window(uid,str(id(self)), url=None, html=None, js_api=None, width=width, height=height, x=None, y=None,
                      resizable=True, fullscreen=False, min_size=(200, 100), hidden=False,
                      frameless=False, easy_drag=True,
                      minimized=False, on_top=False, confirm_close=False, background_color='#FFFFFF',
                      transparent=False, text_select=True, localization=None,
                      zoomable=True, draggable=True, vibrancy=False)
        self.window=window
        self.web_view=EdgeChrome(control,window,None)
        self.control=control
        self.web=self.web_view.web_view
        self.width=width
        self.height=height
        self.parent=parent
        self.chwnd=int(str(self.control.Handle))
        user32.SetParent(self.chwnd,self.winfo_id())
        user32.MoveWindow(self.chwnd,0,0,width,height,True)
        self.loaded=window.events.loaded
        self.__go_bind()
        if url!='':
            self.load_url(url)
        self.core=None

    def __go_bind(self):
        self.bind('<Destroy>',lambda event:self.web.Dispose())
        self.bind('<Configure>',self.__resize_webview)
        self.newwindow=None

    def __resize_webview(self,event):
        user32.MoveWindow(self.chwnd,0,0,self.winfo_width(),self.winfo_height(),True)

    def load_url(self,url):
        self.web_view.load_url(url)

from tkinter import Tk

def main():
    root=Tk()
    root.title('pywebview for tkinter test')
    root.geometry('1200x600+5+5')
    root.config(bg='black')

    frame2 = WebView2(root, 500, 500)
    frame2.pack(side='left', padx=20, fill='both', expand=True)

    def show():


            frame2.load_url('https://github.com/ice-black')

    Button(root, command=show).place(relheight=0.1, relwidth=0.1)



    root.mainloop()

if __name__ == "__main__":

    t = Thread(ThreadStart(main))
    t.ApartmentState = ApartmentState.STA
    t.Start()
    t.Join()


