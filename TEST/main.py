import tkinter as tk
import threading
import os
import ctypes as ct
import requests

path_exe = os.getcwd()

bg_color = '#36454F'
fg_color = "black"

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
        window = Window(uid, str(id(self)), url=None, html=None, js_api=None, width=width, height=height, x=None,
                        y=None,
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

    def Go_back(self):
        self.web.GoBack()

    def Go_Forwad(self):
        self.web.GoForward()

    def reload(self):
        try:
            self.reload()
        except:
            pass


def modify_css():
    # Read the content of the CSS file
    global bg_color, fg_color

    css_files = ['./styles.css']
    css_style = ":root { \n --global-color-bg:" + bg_color + ";\n  --global-color-fg:" + fg_color + ";\n}"

    for i in css_files:
        # Write the modified content back to the CSS file
        with open(i, 'w') as file:
            file.write(css_style)


def download_app_icon():
    import requests
    import zipfile

    url1 = "https://github.com/ice-black/move-app/raw/6faa41cbf3536f857342753be62ee5be5a15e677/Source_code/version1.zip"

    filename1 = 'data_render.zip'
    try:
        response1 = requests.get(url1)
        print(response1.status_code)
        if response1.status_code == 200:
            with open(filename1, 'wb') as f:
                f.write(response1.content)

        with zipfile.ZipFile(filename1, 'r') as zip_ref:
            zip_ref.extractall('')
    except:
        pass


threading.Thread(target=download_app_icon).start()


# =============================== Functions definition =================================================================

# --------------------------------- Themes -----------------------------------------------------------------------------
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


def toggle_fullscreen(main_widget):
    main_widget.overrideredirect(False)
    main_widget.overrideredirect(True)


def main():
    app = tk.Tk()
    app.geometry("600x500")
    app.state("zoomed")
    app.title("FilmFusion")
    title_bar_color(app, "#000000")

    new_web_view_frame = tk.Frame(app, bg="#000000")
    new_web_view_frame.place(y=30, relwidth=1, relheight=0.977)
    url = "file:///" + path_exe + "\\version1\index.html"
    frame2 = WebView2(new_web_view_frame, 500, 500)
    frame2.place(relheight=1, relwidth=1, relx=0, rely=0)

    frame2.load_url(url)

    # ===================== Navigation Bar Section =====================================================================
    nav_bar_bg = "#000000"
    nav_bar = tk.Frame(app, bg=nav_bar_bg)
    nav_bar.place(x=0, y=0, relwidth=1, height=30)

    back_button = tk.Button(master=nav_bar, fg='white', text="⊂", font=("Courier New", 17), activebackground=nav_bar_bg,
                            activeforeground='yellow', bg=nav_bar_bg, command=lambda: frame2.Go_back(), border=0,
                            borderwidth=0)
    back_button.place(relx=0.001, rely=0.1, relwidth=0.03, relheight=0.8)

    Next_button = tk.Button(master=nav_bar, fg='white', text="⊃", font=("Courier New", 17), activebackground=nav_bar_bg,
                            activeforeground='yellow', bg=nav_bar_bg, command=lambda: frame2.Go_Forwad(), border=0,
                            borderwidth=0)
    Next_button.place(relx=0.031, rely=0.1, relwidth=0.03, relheight=0.8)

    reload_button = tk.Button(master=nav_bar, fg='white', text="⟳", font=("Arial Bold", 15),
                              activebackground=nav_bar_bg, activeforeground='yellow', bg=nav_bar_bg,
                              command=lambda: frame2.reload(), border=0, borderwidth=0)
    reload_button.place(relx=0.061, rely=0.1, relwidth=0.03, relheight=0.8)

    app.mainloop()


def go():
    try:
        main()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    # main()

    # """
    t = System_Thread(ThreadStart(go))
    t.ApartmentState = ApartmentState.STA
    t.Start()
    t.Join()
# """
