from tkinter import Tk
import clr
from tkwebview2.tkwebview2 import WebView2, have_runtime, install_runtime
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Threading')
from System.Windows.Forms import Control
from System.Threading import Thread, ApartmentState, ThreadStart

# Event handler for when the web page finishes loading
def on_navigation_completed(sender, args):
    print("Navigation completed.")
    # You can perform actions here after the page has loaded

# Event handler for when a message is received from the web page
def on_web_message_received(sender, args):
    print("Received message from web page:", args.Message)
    # You can process and respond to messages received from the web page here

# Event handler for when the web view requests external navigation (e.g., clicking a link)
def on_navigation_starting(sender, args):
    print("Navigation starting to:", args.Uri)
    # You can prevent navigation or perform actions before navigating here

# Event handler for when the web page title changes
def on_document_title_changed(sender, args):
    print("Document title changed to:", args.Title)
    # You can update your application's title or perform other actions here

def main():
    if not have_runtime():
        install_runtime()
    root = Tk()
    root.title('tkwebview2 Event Capture')
    root.geometry('1200x600+5+5')

    frame2 = WebView2(root, 500, 500)
    frame2.pack(side='left', padx=20, fill='both', expand=True)

    # Bind event handlers to WebView2 events
    frame2.NavigationCompleted += on_navigation_completed
    frame2.WebMessageReceived += on_web_message_received
    frame2.NavigationStarting += on_navigation_starting
    frame2.DocumentTitleChanged += on_document_title_changed

    frame2.load_url('https://vidsrc.to/embed/movie/tt8385148')

    root.mainloop()

if __name__ == "__main__":
    t = Thread(ThreadStart(main))
    t.ApartmentState = ApartmentState.STA
    t.Start()
    t.Join()

