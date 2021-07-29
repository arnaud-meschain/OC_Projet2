import urllib.request
from bs4 import BeautifulSoup
import re
from scrap_page import scraper_page
import csv

urlcategory = input("url catégorie à scraper:")
urlcategoryBase = urlcategory.replace('/index.html','')
urlpageslist = []

response = urllib.request.urlopen(urlcategory)
soup = BeautifulSoup(response, 'html.parser')

#extraction des url de la première page:
urlpages = soup.find_all("article", class_="product_pod")
for url in urlpages:
	urlpagerelative = url.h3.find("a")["href"]
	urlpage = re.sub(r"../../../", "https://books.toscrape.com/catalogue/", urlpagerelative)
	urlpageslist.append(urlpage)

#recherche et extraction des url d'autres pages:
while soup.find("li", {"class": "next"}) != None:
	urlcategory = urlcategoryBase+"/"+soup.find("li", {"class": "next"}).a["href"]
	response = urllib.request.urlopen(urlcategory)
	soup = BeautifulSoup(response, 'html.parser')
	urlpages = soup.find_all("article", class_="product_pod")
	for url in urlpages:
		urlpagerelative = url.h3.find("a")["href"]
		urlpage = re.sub(r"../../../", "https://books.toscrape.com/catalogue/", urlpagerelative)
		urlpageslist.append(urlpage)

#Nom de repertoire pour la categorie
category = soup.find('h1').text

#Nom de fichier csv pour la categorie:
category_csv = str(category +".csv")

#ecriture des données dans le fichier csv
#labels = ['product_page_url', 'universal_ product_code', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
with open(category_csv, 'w', newline='', encoding='utf-8') as f:
	fieldnames = ['product_page_url', 'universal_ product_code', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
	thewriter = csv.DictWriter(f, fieldnames=fieldnames)
	thewriter.writeheader()
for urlpage in urlpageslist:
	#ecriture du fichier CSV:
	scrap_page = {}
	scrap_page = scraper_page(urlpage)
	with open(category_csv, 'a', newline='', encoding='utf-8') as csvfile:
		thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
		thewriter.writerow(scrap_page)
print('le fichier ',category_csv, ' a été créé')