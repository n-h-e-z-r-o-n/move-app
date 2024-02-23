import requests
def download_app_icon():
    url1 = "https://github.com/ice-black/move-app/blob/9af6998c123fd6f2d86ff9a083eecd094200a8ab/Assets/tx.ico"
    url2 = "https://github.com/ice-black/move-app/blob/be16bd596a33e02576b6935c15efeb39a212fbf9/Assets/startup.jpg"
    url3 = "https://github.com/ice-black/move-app/blob/a469eb9d2b5ede618e0c1efd17a854e3134c2c5f/Assets/footer.jpg"
    url4 = "https://github.com/ice-black/move-app/blob/a469eb9d2b5ede618e0c1efd17a854e3134c2c5f/Assets/search_animation.gif"
    filename1 = 'tx.ico'
    filename2 = 'startup.jpg'
    filename3 = 'footer.jpg'
    filename4 = "search_animation.gif"
    while True:
        try:
            response1 = requests.get(url1)
            with open(filename1, 'wb') as f:
                f.write(response1.content)

            response2 = requests.get(url2)
            with open(filename2, 'wb') as f:
                f.write(response2.content)

            response3 = requests.get(url3)
            with open(filename3, 'wb') as f:
                f.write(response3.content)
            response4 = requests.get(url4)
            with open(filename4, 'wb') as f:
                f.write(response4.content)
            break

        except:
            pass
download_app_icon()