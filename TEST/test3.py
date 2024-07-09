import requests
import zipfile
import io
import os


def download_and_extract_zip(url, extract_to='.'):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Create a ZipFile object from the downloaded bytes
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            # Extract all contents into the specified directory
            z.extractall(extract_to)
        print(f"Files extracted to {os.path.abspath(extract_to)}")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")


# URL of the zip file to download
url = "https://drive.google.com/file/d/1tBO1qMaimN-CoKq3w7Kkitu-dCE_V9Y9/view?usp=drive_link"
# Folder where the contents will be extracted
extract_to = 'Source_code'

# Call the function to download and extract the zip file
download_and_extract_zip(url, extract_to)


