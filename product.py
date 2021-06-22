import requests
from bs4 import BeautifulSoup

#url = 'http://books.toscrape.com/index.html'
#url = 'http://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html'
url = 'http://books.toscrape.com/catalogue/the-last-painting-of-sara-de-vos_259/index.html'

def category_urls(url):

    response = requests.get(url)
    if response.ok:
        links = []
        soup = BeautifulSoup(response.text, 'html.parser')
        lis = soup.find("ul", {"class": "nav nav-list"}).find_all("a")
        for li in lis:

            link = li['href']
            links.append("http://books.toscrape.com/" + str(link))
        return links


def nbr_pages(url):
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        strong = soup.find_all("strong")
        x = int(strong[1].text)
        return (x // 20) + (x % 20 != 0)


def category_pages_urls(url):
    pages = []
    pages.append(url)
    if nbr_pages(url) > 1:
        for i in range(1, nbr_pages(url)):
            pages.append(url.replace("index", "page-" + str(i+1)))
    return pages


def product_urls(url):

    response = requests.get(url)
    if response.ok:
        products = []
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all("article", {"class": "product_pod"})
        for article in articles:
            ref = article.find("a")
            link = ref["href"]
            products.append("http://books.toscrape.com/catalogue" + str(link[8:]) + "\n")
        return products


def products_meta(url):
    response = requests.get(url)
    if response.ok:
        links = []
        soup = BeautifulSoup(response.text, 'html.parser')
        image = soup.find("div", {"id": "product_gallery"})
        image_link = image.find('img', {"attrs": "src"})
        return image_link


print(products_meta(url))






"""def all_urls(url):
    all = []

    for i in category_urls(url):
        x = 0
        while x <= nbr_pages(i):
            all.append(category_pages_urls(i)[x])
        x += 1
    print(all)

all_urls(url)"""
