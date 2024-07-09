


def download_app_icon():
    import requests
    import zipfile

    url1 = "https://github.com/ice-black/move-app/raw/6faa41cbf3536f857342753be62ee5be5a15e677/Source_code/version1.zip"

    filename1='data_render.zip'
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





download_app_icon()