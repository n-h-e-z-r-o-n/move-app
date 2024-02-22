import requests
internet_check = False
def has_internet_connection():
    try:
        response = requests.get("https://www.google.com", timeout=3)
        internet_check =  response.status_code == 200  # Check for successful response (200)
    except Exception as e:
        internet_check = False  # Handle exceptions gracefully

if internet_check:
    print("Connected to the internet!")
else:
    print("No internet connection.")