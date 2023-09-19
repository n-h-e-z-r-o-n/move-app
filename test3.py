import tkinter as tk
from webview2.core import WebView2

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("400x300")

        self.webview2 = WebView2()
        self.webview2.grid(row=0, column=0, sticky="NSEW")

        # Register an event handler for the NavigationStarting event.
        self.webview2.NavigationStarting += self.on_navigation_starting

        self.root.mainloop()

    def on_navigation_starting(self, sender, args):
        # Get the URL that the WebView2 is navigating to.
        url = args.Uri

        # Print the URL to the console.
        print("Navigating to:", url)

if __name__ == "__main__":
    app = App()