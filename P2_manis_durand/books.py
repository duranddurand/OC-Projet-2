import requests
from bs4 import BeautifulSoup

url = 'http://books.toscrape.com/index.html'

response = requests.get(url)
if response.ok:
    links = []
    soup = BeautifulSoup(response.text, 'html.parser')
    lis = soup.find_all('li')
    for li in lis:
        a = li.find('a')
        link = a['href']
        links.append(link)
    print(links)
