import requests

def has_internet_connection():
    try:
        response = requests.get("https://www.google.com", timeout=3)
        return response.status_code == 200  # Check for successful response (200)
    except Exception as e:
        return False  # Handle exceptions gracefully

if has_internet_connection():
    print("Connected to the internet!")
else:
    print("No internet connection.")