import requests
import concurrent.futures
import urllib.request
import re
import csv
from bs4 import BeautifulSoup

path = "/Users/duranmanis/Desktop/Python/P2_manis_durand/"


def category_urls(url):
    # input : website url[]
    # output : url for each category[]

    response = requests.get(url)

    if response.ok:
        categories = []
        soup = BeautifulSoup(response.text, 'html.parser')
        urls = soup.find("ul", {"class": "nav nav-list"}).find_all("a")[1:]
        for url in urls:
            categories.append("http://books.toscrape.com/" + str(url['href']))
        return categories


def nbr_pages(url):
    # input : category url
    # output : nbr of pages per category

    response = requests.get(url)

    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        strong = soup.find_all("strong")
        x = int(strong[1].text)
        return (x // 20) + (x % 20 != 0)


def category_pages(url):
    # input: category url
    # output: category pages url

    pages = [url]

    if nbr_pages(url) > 1:
        for i in range(1, nbr_pages(url)):
            pages.append(url.replace("index", "page-" + str(i+1)))
    return pages


def product_urls(url):
    # input : category page url
    # output : product urls

    response = requests.get(url)

    if response.ok:

        products = []
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all("article", class_="product_pod")
        for article in articles:
            ref = article.find("a")
            link = ref["href"]
            products.append("http://books.toscrape.com/catalogue" + link[8:])
        return products

images = []

def product_meta(url):
    # input = product url
    # output = dict of product's meta

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    upc = soup.find("th", text="UPC").find_next_sibling("td").text
    title = soup.find("div", class_="product_main").find("h1").text
    price_incl = soup.find("th", text="Price (incl. tax)").find_next_sibling().text
    price_excl = soup.find("th", text="Price (excl. tax)").find_next_sibling().text

    stock = re.sub("\\D", "", soup.find("div", class_="product_main").find("p", class_="instock").text)
    description = soup.find("article", class_="product_page").find("div", class_="sub-header").find_next_sibling().text
    category_ = soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()
    rating = (str({"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
                  .get(soup.find("p", class_="star-rating")["class"][1])) + "/5")
    img_src = "http://books.toscrape.com/" + (soup.find("div", class_="carousel").find("img"))["src"][6:]
    images.append(img_src)

    return {"product_page_url": url, "universal_product_code": upc, "title": title, "price_including_tax": price_incl,
            "price_excluding_tax": price_excl, "number_available": stock, "product_description": description,
            "category": category_, "review_rating": rating, "image_url": img_src}


def create_csv(url):
    # input = category url
    # output = csv of all products meta
    books = []

    for page in category_pages(url):
        for url in product_urls(page):
            books.append(url)

    meta = product_meta(books[0])
    filepath = path + "csv/" + meta["category"] + ".csv"
    
    with open(filepath, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=meta.keys())
        writer.writeheader()
        for book in books:
            writer.writerow(product_meta(book))


def create_jpg(image):

    jpeg = urllib.request.urlopen(image)
    with open(path + "images/" + image.split("/")[-1], "wb") as f:
        f.write(jpeg.read())


def main():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        tables = executor.map(create_csv, category_urls('http://books.toscrape.com/index.html'))
    with concurrent.futures.ThreadPoolExecutor() as executor:
        frames = executor.map(create_jpg, images)

main()

