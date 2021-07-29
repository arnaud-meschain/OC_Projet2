#from typing import Container
import urllib.request
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from scrap_page import scraper_page
from scrap_category import scraper_category
import csv
import os
from time import sleep

urlsite = 'https://books.toscrape.com'
urlcategorylist = []
#demande si l'on veut garder l'image du livre puis l'enregistre si Y
img_check = str(input("Voulez vous enregistrer l'image ? (Y/N): ")).lower().strip()
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
	#demande de saisie de l'url de la categorie:
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
	print('le fichier ', category_csv, ' est créé')

	if img_check == 'y':
		os.makedirs(str(category)) #creation du repertoire pour les images		
		for urlpage in urlpageslist:
			returned_page = scraper_page(urlpage)
			scrap_page = returned_page[0]
			with open(category_csv, 'a', newline='', encoding='utf-8') as csvfile:
				thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
				thewriter.writerow(scrap_page)
			#enregistrement des images:
			title_img = returned_page[3]
			url_img = returned_page[2]
			title_img_path = os.path.join(os.getcwd()+"/"+category, title_img)
			urllib.request.urlretrieve(url_img, title_img_path)
			sleep(0.05)#moduler le temps de sleep si l'écriture des données pose problème
		print("les images sont enregistrées dans : ", category)
print('fin')