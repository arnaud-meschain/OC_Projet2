import urllib.request
from bs4 import BeautifulSoup
import re
from scrap_page import scraper_page
import csv
import os
from time import sleep

#fonction qui extrait les données d'une categorie sous forme de bibliothèque, réutilisée par les autres scripts
def scraper_category(urlcategory):

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
		sleep(0.02)
		for url in urlpages:
			urlpagerelative = url.h3.find("a")["href"]
			urlpage = re.sub(r"../../../", "https://books.toscrape.com/catalogue/", urlpagerelative)
			urlpageslist.append(urlpage)

	#Nom de repertoire pour la categorie
	category = soup.find('h1').text

	#Nom de fichier csv pour la categorie:
	category_csv = str(category +".csv")
	
	return(urlpageslist, category, category_csv)

#utilisation manuelle du script pour une categorie:
if __name__ == "__main__":

	#demande de saisie de l'url de la categorie et si on enregistre les jpg:
	urlcategory = input("url catégorie à scraper:")
	img_check = str(input("Voulez vous enregistrer les images ? (Y/N): ")).lower().strip()

	#recuperation du contenu de la categorie
	returned_category = scraper_category(urlcategory)
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
		#ecriture du fichier CSV:
		scrap_page = {}
		scrap_page = scraper_page(urlpage)[0]
		with open(category_csv, 'a', newline='', encoding='utf-8') as csvfile:
			thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
			thewriter.writerow(scrap_page)
		sleep(0.05)# moduler le temps d'arrêt si l'écriture du CSV pose problème

	#choix si l'on veut garder les images puis les enregistre si Y
	if img_check == 'y':
		os.makedirs(str(category)) #creation du repertoire pour les images
		print("les images sont enregistrées dans : ", os.getcwd(), category)
		for urlpage in urlpageslist:
			#nom de fichier jpg
			title_img = scraper_page(urlpage)[3]
			#recupération url
			url_img = scraper_page(urlpage)[2]
			title_img_path = os.path.join(os.getcwd()+"/"+category, title_img)
			urllib.request.urlretrieve(url_img, title_img_path)
	elif img_check == 'n':
		print("les images ne seront pas enregistrées")
	else:
		print("Commande invalide: les images ne seront pas enregistrées")