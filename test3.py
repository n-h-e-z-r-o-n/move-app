import webview

if __name__ == '__main__':
    # Create a standard webview window

    window = webview.create_window('Simple browser', 'https://vidsrc.to/embed/movie/tt8385148')
    window.toggle_fullscreen()
    webview.start()

