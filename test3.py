import webview
import time
"""
This example demonstrates how to handle pywebview events.
"""

def on_closed():
    print('pywebview window is closed')


def on_closing():
    print('pywebview window is closing')


def on_shown():
    print('pywebview window shown')


def on_minimized():
    print('pywebview window minimized')


def on_restored():
    print('pywebview window restored')


def on_maximized():
    print('pywebview window maximized')





def on_resized(width, height):
    print('pywebview window is resized. new dimensions are {width} x {height}'.format(width=width, height=height))


def on_moved(x, y):
    print('pywebview window is moved. new coordinates are x: {x}, y: {y}'.format(x=x, y=y))


if __name__ == '__main__':
    window = webview.create_window('Simple browser', 'https://vidsrc.to/embed/movie/tt8385148', confirm_close=True)

    window.events.closed += on_closed
    window.events.closing += on_closing
    window.events.shown += on_shown

    window.events.minimized += on_minimized
    window.events.maximized += on_maximized
    window.events.restored += on_restored
    window.events.resized += on_resized
    window.events.moved += on_moved

    webview.start()





