import tkinter as tk
import threading
import os
import ctypes as ct

path_exe = os.getcwd()
bg_color = '#36454F'
fg_color = "black"

# ---------------------------------------------- HTTP_ Local Server  -------------------------------------------------------------------------
httpd = None
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import base64
from PIL import Image
from io import BytesIO


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        global llm_chain, clinical_Note_upload_btn, proccessed_img_url
        if self.path == '/':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            received_data = data.get('data')  # Extract the data received from the HTML form
            #print("Data received from HTML:", received_data)

            if received_data.startswith("image_Bit"):
                received_data = received_data.replace("image_Bit", '')

                base64_data = received_data.replace('data:image/jpeg;base64,', '')
                base64_data = base64_data.replace('data:image/png;base64,', '')
                base64_data = base64_data.replace('data:image/jpg;base64,', '')

                # Decode the base64 data
                image_data = base64.b64decode(base64_data)

                # Open the image using PIL
                image = Image.open(BytesIO(image_data))

                # Save the image to the specified output path
                image.save("./local_img.jpg")
                proccessed_img_url = os.getcwd() + "/local_img.jpg"
                clinical_Note_upload_btn.invoke()
                processed_data = " Img Recived"
            else:
                if llm_chain is None:
                    llm_inference_initializ()

                Answer = llm_chain.invoke(input=f"{received_data}")
                Answer = Answer['text']

                processed_data = Answer.replace("\n", "<br>")
                if "|" in processed_data:
                    table = "<table>"
                    rows = processed_data.split("<br>")
                    headers = "<tr>" + "<th>" + "</th><th>".join(rows[0].split("|")) + "</th>" + "</tr>"
                    table_rows = ''
                    for row in rows[1:]:
                        table_rows += "<tr>"
                        table_rows += "<td>" + "</td><td>".join(row.split("|")) + "</td>"
                        table_rows += "</tr>"

                    table += headers + table_rows
                    table += "</table>"
                    processed_data = table

            # Print the received data and the processed data

            print("Processed data:", processed_data)

            # Send a response back to the client
            response_data = {'message': 'Data received and processed successfully', 'processed_data': processed_data}
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')  # Allow requests from any origin
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        else:
            self.send_error(404, "Not found")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()


def run_server():
    def run_server_thread():
        global httpd
        print("server_running")
        server_address = ('localhost', 8080)
        httpd = HTTPServer(server_address, RequestHandler)
        httpd.serve_forever()
        print("server_stopped")

    threading.Thread(target=run_server_thread).start()
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