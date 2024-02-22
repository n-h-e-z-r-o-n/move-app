import socket

def check_internet_connection(host="8.8.8.8", port=23, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False

# Check internet connection
if check_internet_connection():
    print("Internet connection available")
else:
    print("No internet connection")