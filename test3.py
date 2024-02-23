"""
from requests import get
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
url = 'https://www.imdb.com/title/tt1439629/episodes?season=1'
response = get(url, headers=header)
print(response)
from bs4 import BeautifulSoup

html_soup = BeautifulSoup(response.text, 'html.parser')
type(html_soup  )

episode_containers = html_soup.find_all('div', class_="ipc-tabs ipc-tabs--base ipc-tabs--align-left ipc-tabs--display-chip ipc-tabs--inherit")
print(episode_containers)
"""
import imdb_extract