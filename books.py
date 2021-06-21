import requests
from bs4 import BeautifulSoup

url = 'http://books.toscrape.com/index.html'

response = requests.get(url)
if response.ok:
    links = []
    soup = BeautifulSoup(response.text, 'html.parser')
    lis = soup.find("ul", {"class":"nav nav-list"}).find_all("a")
    print(len(lis))
    for li in lis:
        link = li['href']
        links.append( "http://books.toscrape.com/" + str(link) + "\n")

        print( "http://books.toscrape.com/" + str(link) + "\n")

