import webview
import time

def toggle_fullscreen(window):
    # wait a few seconds before toggle fullscreen:
    time.sleep(5)

    window.toggle_fullscreen()


if __name__ == '__main__':
    window = webview.create_window('Simple browser', 'https://vidsrc.to/embed/movie/tt8385148')

    webview.start(toggle_fullscreen, window)




