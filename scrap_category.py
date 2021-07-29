import urllib.request
from bs4 import BeautifulSoup
import re
from scrap_page import scraper_page

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
		for url in urlpages:
			urlpagerelative = url.h3.find("a")["href"]
			urlpage = re.sub(r"../../../", "https://books.toscrape.com/catalogue/", urlpagerelative)
			urlpageslist.append(urlpage)

	#Nom de repertoire pour la categorie
	category = soup.find('h1').text

	#Nom de fichier csv pour la categorie:
	category_csv = str(category +".csv")
	
	return(urlpageslist, category, category_csv)