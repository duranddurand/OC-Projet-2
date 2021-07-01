import requests
import re
import csv
from bs4 import BeautifulSoup

# input : website url[]
# output : url for each category[]


def category_urls(url):

    response = requests.get(url)
    if response.ok:
        categories = []
        soup = BeautifulSoup(response.text, 'html.parser')
        urls = soup.find("ul", {"class": "nav nav-list"}).find_all("a")[1:]
        for url in urls:
            categories.append("http://books.toscrape.com/" + str(url['href']))
        return categories


# input : category url
# output : nbr of pages per category


def nbr_pages(url):
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        strong = soup.find_all("strong")
        x = int(strong[1].text)
        return (x // 20) + (x % 20 != 0)


# input: category url
# output: category pages url


def category_pages(url):
    pages = [url]
    if nbr_pages(url) > 1:
        for i in range(1, nbr_pages(url)):
            pages.append(url.replace("index", "page-" + str(i+1)))
    return pages


# input : category page url
# output : product urls


def product_urls(url):

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


# input = product url
# output = dict of product's meta


def product_meta(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    upc = soup.find("th", text="UPC").find_next_sibling("td").text
    title = soup.find("div", class_="product_main").find("h1").text
    price = soup.find("div", class_="product_main").find("p", class_="price_color").text[1:]
    stock = re.sub("\\D", "", soup.find("div", class_="product_main").find("p", class_="instock").text)
    description = soup.find("div", id="product_description").find_next_sibling("p").text
    category_ = soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()
    rating = (str({"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
                  .get(soup.find("p", class_="star-rating")["class"][1])) + "/5")
    img_src = "http://books.toscrape.com/" + (soup.find("div", class_="carousel").find("img"))["src"][6:]

    return {"product_page_url": url, "universal_product_code": upc, "title": title, "price_including_tax": price,
            "price_excluding_tax": price, "number_available": stock, "product_description": description,
            "category": category_, "review_rating": rating, "image_url": img_src}
# print(product_meta('http://books.toscrape.com/catalogue/sophies-world_966/index.html'))
# input = category url
# output = csv of all products meta


def create_csv(url):

    books = []

    for page in category_pages(url):
        for url in product_urls(page):
            books.append(url)

    meta = product_meta(books[0])

    filepath = "/Users/duranmanis/Desktop/Python/P2_manis_durand/csv/" + meta["category"] + ".csv"
    
    with open(filepath, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=meta.keys())
        writer.writeheader()
        for book in books:
            writer.writerow(product_meta(book))


for category in category_urls('http://books.toscrape.com/index.html')[0:1]:
    create_csv(category)
