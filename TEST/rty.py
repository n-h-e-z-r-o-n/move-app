import requests


def download_app_icon():
    url1 = "https://drive.google.com/file/d/1tBO1qMaimN-CoKq3w7Kkitu-dCE_V9Y9/view?usp=drive_link"




    try:
        response1 = requests.get(url1)
        print(response1.status_code)
        if response1.status_code == 200:
            with open(filename1, 'wb') as f:
                f.write(response1.content)



    except:
        break


download_app_icon()