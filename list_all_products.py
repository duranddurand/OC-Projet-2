import requests
import re
import csv
from bs4 import BeautifulSoup

#url = 'http://books.toscrape.com/index.html'
#url = 'http://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html'
#
url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'

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


#input: Category url from sidebar
#output: returns a list of all pages
def category_pages_urls(url):
    pages = [url]
    if nbr_pages(url) > 1:
        for i in range(1, nbr_pages(url)):
            pages.append(url.replace("index", "page-" + str(i+1)))
    return pages


def product_urls(url):

    response = requests.get(url)
    if response.ok:

        products = []
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all("article", class_="product_pod")
        for article in articles:
            ref = article.find("a")
            link = ref["href"]
            products.append("http://books.toscrape.com/catalogue" + link[8:] + "\n")
        return products


def products_meta(url):

    response = requests.get(url)
<<<<<<< HEAD:list_all_products.py
    soup = BeautifulSoup(response.text, 'html.parser')

    UPC = soup.find("th", text="UPC").find_next_sibling("td").text
    title = soup.find("div", class_="product_main").find("h1").text
    price = soup.find("div", class_="product_main").find("p", class_="price_color").text[1:]
    instock = re.sub("\D", "", (soup.find("div", class_="product_main").find("p", class_="instock").text))
    description = soup.find(id="product_description").find_next_sibling("p").text
    category = soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()
    rating = str({"One":1, "Two":2, "Three":3, "Four":4, "Five":5}.get(soup.find("p", class_="star-rating")["class"][1])) + "/5"
    img_src = "http://books.toscrape.com/" + (soup.find("div", class_="carousel").find("img"))["src"][6:]

    return {"product_page_url":url,"universal_ product_code":UPC,"title":title,"price_including_tax":price,"price_excluding_tax":price,"number_available":instock, "product_description":description,"category":category, "review_rating":rating,"image_url":img_src}

row = [products_meta(url)]

def create_csv(url):

    #filename = row[0]["category"] + ".csv"

    with open(row[0]["category"] + ".csv", 'w', ) as f:
        writer = csv.DictWriter(f, row[0].keys())
        writer.writeheader()
        for d in row:
            writer.writerow(d)

create_csv(url)
=======
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        image_src = "http://books.toscrape.com/" + (soup.find("div", class_="carousel").find("img"))["src"][6:]
        title = soup.find("div", class_="product_main").find("h1").text
        price = soup.find("div", class_="product_main").find("p", class_="price_color").text[1:]
        instock = re.sub("\D", "", (soup.find("div", class_="product_main").find("p", class_="instock").text))

        return (title, image_src, price, price, instock)

print(products_meta(url))

"""
all_urls(url):
all = []

    for i in category_urls(url):
        x = 0
        while x <= nbr_pages(i):
            all.append(category_pages_urls(i)[x])
        x += 1
    print(all)

all_urls(url)
"""
>>>>>>> origin/main:product.py
