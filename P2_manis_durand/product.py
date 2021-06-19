import requests
from bs4 import BeautifulSoup

url = 'http://books.toscrape.com/index.html'

def links_categorys(url):
    response = requests.get(url)
    if response.ok:
        links = []
        soup = BeautifulSoup(response.text, 'html.parser')
        lis = soup.find("ul", {"class":"nav nav-list"}).find_all("a")
        for li in lis:
            link = li['href']
            links.append( "http://books.toscrape.com/" + str(link) + "\n")
    return( "http://books.toscrape.com/" + str(link) + "\n")

def nbr_pages(url):
    response = requests.get(url)
    if response.ok:
        links = []
        soup = BeautifulSoup(response.text, 'html.parser')
        strongs = soup.find_all("strong")
        x = int(strongs[1].text)
        return ((x // 20) + (x % 20 != 0))

def category_pages(url):
    pages = []
    pages.append(url)
    if (nbr_pages(url) > 1):
        for i in range(1, nbr_pages(url)):
            pages.append(url.replace("index", "page-" + str(i+1)))
    return pages


def links_products(url):

    response = requests.get(url)
    if response.ok:
        links = []
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all("article", {"class":"product_pod"})
        for article in articles:
            ref = article.find("a")
            link = ref["href"]
            links.append("http://books.toscrape.com/catalogue" + str(link[8:]) + "\n")
    return links






