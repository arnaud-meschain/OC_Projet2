#from typing import Container
import urllib.request
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from scrap_page import scraper_page
from scrap_category import scraper_category
import csv
from time import sleep

urlsite = 'https://books.toscrape.com'
urlcategorylist = []

response = urllib.request.urlopen(urlsite)
soup = BeautifulSoup(response, 'html.parser')

#extraction des url des categories:
urlcategoriesul = soup.find("ul", class_="nav nav-list")
urlcategories = urlcategoriesul.find_all("li")

#création de la liste des urls de categorie

for url in urlcategories:
	urlcategoryrelative = url.find("a")["href"]
	urlcategory = urljoin("https://books.toscrape.com/",urlcategoryrelative)
	urlcategorylist.append(urlcategory)

del urlcategorylist[0] #suppression 'https://books.toscrape.com/catalogue/category/books_1/index.html'

#recupération des données:

for url in urlcategorylist:
	#saisie de l'url de la categorie:
	urlcategory = url
	returned_category = scraper_category(urlcategory)
	#recuperation du contenu de la categorie
	urlpageslist = returned_category[0]

	#titre pour nommer le CSV
	category = returned_category[1]
	category_csv = returned_category[2]

	#ecriture des données dans le fichier csv
	#labels = ['product_page_url', 'universal_ product_code', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
	with open(category_csv, 'w', newline='', encoding='utf-8') as f:
		fieldnames = ['product_page_url', 'universal_ product_code', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
		thewriter = csv.DictWriter(f, fieldnames=fieldnames)
		thewriter.writeheader()
	for urlpage in urlpageslist:
		returned_page = scraper_page(urlpage)
		scrap_page = returned_page
		with open(category_csv, 'a', newline='', encoding='utf-8') as csvfile:
			thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
			thewriter.writerow(scrap_page)
		sleep(0.05)#moduler le temps de sleep si l'écriture des données pose problème
	print('fichier ',category_csv, ' créé' )
print('fin')