import webview

if __name__ == '__main__':
    # Create a standard webview window

    window = webview.create_window('Simple browser', 'https://pywebview.flowrl.com/hello')
    window.toggle_fullscreen()
    webview.start()

