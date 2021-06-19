import requests
from bs4 import BeautifulSoup

url = 'http://books.toscrape.com/index.html'

response = requests.get(url)

print (response)
