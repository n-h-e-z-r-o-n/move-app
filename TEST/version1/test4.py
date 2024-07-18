import requests
def download_app_icon():
    url1 = "https://github.com/ice-black/move-app/tree/main/Source_code"

    folder = 'Source_code'

    try:
        response1 = requests.get(url1)
        with open(folder, 'wb') as f:
            f.write(response1.content)
    except:
        pass


download_app_icon()