import tkinter as tk
import threading
import os
import ctypes as ct

path_exe = os.getcwd()
bg_color = '#36454F'
fg_color = "black"

# ---------------------------------------------- HTTP_ Local Server  -------------------------------------------------------------------------

# ------------------------------- web-Integration ---------------------------------------------------------------------------------------------------

import ctypes
from webview.window import Window
from webview.platforms.edgechromium import EdgeChrome
from System import IntPtr, Int32, Func, Type, Environment
from System.Windows.Forms import Control
from System.Threading import ApartmentState, ThreadStart, SynchronizationContext, SendOrPostCallback
from System.Threading import Thread as System_Thread

user32 = ctypes.windll.user32


class WebView2(tk.Frame):
    def __init__(self, parent, width: int, height: int, url: str = '', **kw):
        global bg_color
        tk.Frame.__init__(self, parent, width=width, height=height, **kw)
        control = Control()
        uid = 'master'
        window = Window(uid, str(id(self)), url=None, html=None, js_api=None, width=width, height=height, x=None, y=None,
                        resizable=True, fullscreen=False, min_size=(200, 100), hidden=False,
                        frameless=False, easy_drag=True,
                        minimized=False, on_top=False, confirm_close=False, background_color=bg_color,
                        transparent=False, text_select=True, localization=None,
                        zoomable=True, draggable=True, vibrancy=False)
        self.window = window
        self.web_view = EdgeChrome(control, window, None)
        self.control = control
        self.web = self.web_view.web_view
        self.width = width
        self.height = height
        self.parent = parent
        self.chwnd = int(str(self.control.Handle))
        user32.SetParent(self.chwnd, self.winfo_id())
        user32.MoveWindow(self.chwnd, 0, 0, width, height, True)
        self.loaded = window.events.loaded
        self.__go_bind()
        if url != '':
            self.load_url(url)
        self.core = None
        self.web.CoreWebView2InitializationCompleted += self.__load_core

    def __go_bind(self):
        self.bind('<Destroy>', lambda event: self.web.Dispose())
        self.bind('<Configure>', self.__resize_webview)
        self.newwindow = None

    def __resize_webview(self, event):
        user32.MoveWindow(self.chwnd, 0, 0, self.winfo_width(), self.winfo_height(), True)

    def __load_core(self, sender, _):
        self.core = sender.CoreWebView2
        self.core.NewWindowRequested -= self.web_view.on_new_window_request
        # Prevent opening new windows or browsers
        self.core.NewWindowRequested += lambda _, args: args.Handled(True)

        if self.newwindow != None:
            self.core.NewWindowRequested += self.newwindow
        settings = sender.CoreWebView2.Settings  # 设置
        settings.AreDefaultContextMenusEnabled = False  # 菜单
        settings.AreDevToolsEnabled = False  # 开发者工具
        # self.core.DownloadStarting+=self.__download_file

    def load_url(self, url):
        self.web_view.load_url(url)

    def reload(self):
        self.core.Reload()


def modify_css():
    # Read the content of the CSS file
    global bg_color, fg_color

    css_files = ['./styles.css']
    css_style = ":root { \n --global-color-bg:" + bg_color + ";\n  --global-color-fg:" + fg_color + ";\n}"

    for i in css_files:
        # Write the modified content back to the CSS file
        with open(i, 'w') as file:
            file.write(css_style)

# =============================== Functions definition ============================================================================================

# --------------------------------- Themes --------------------------------------------------------------------------------------------------------
def title_bar_color(window, color):
    # import ctypes as ct
    try:
        window.update()
        if color.startswith('#'):
            blue = color[5:7]
            green = color[3:5]
            red = color[1:3]
            color = blue + green + red
        else:
            blue = color[4:6]
            green = color[2:4]
            red = color[0:2]
            color = blue + green + red
        get_parent = ct.windll.user32.GetParent
        HWND = get_parent(window.winfo_id())

        color = '0x' + color
        color = int(color, 16)

        ct.windll.dwmapi.DwmSetWindowAttribute(HWND, 35, ct.byref(ct.c_int(color)), ct.sizeof(ct.c_int))

    except Exception as e:
        print("title_bar_color fun error : ", e)


def Main():
    global  bg_color
    app = tk.Tk()

    screen_width = app.winfo_screenwidth()  # Get the screen width dimensions
    screen_height = app.winfo_screenheight()

    view = WebView2(app, width=screen_width, height=screen_height)
    view.place(relheight=1, relwidth=1)

    view.load_url('file:///' + path_exe+'./index.html')
    #view.load_url( "https://vidsrc.to/embed/tv/tt11198330")
    title_bar_color(app, bg_color)
    modify_css()

    app.mainloop()

def go():
    try:
      Main()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    #main()

    #"""
        t = System_Thread(ThreadStart(go))
        t.ApartmentState = ApartmentState.STA
        t.Start()
        t.Join()
    # """