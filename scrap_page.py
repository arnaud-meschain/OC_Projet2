import urllib.request
from bs4 import BeautifulSoup
import re
import csv

#fonction qui extrait les données d'une page sous forme de bibliothèque, réutilisée par les autres scripts
def scraper_page(urlpage):

	response = urllib.request.urlopen(urlpage)
	soup = BeautifulSoup(response, "html.parser")
	
	#recherche category

	categories = soup.select("a", {"class": "breadcrumb"})
	category = categories [3]

	# recherche du review rating
	soupreview = soup.find("div", {"class": "col-sm-6 product_main"})

	if soupreview.find("p", {"class": "star-rating Five"}):
		review_rating = '5 star'
	elif soupreview.find("p", {"class": "star-rating Four"}):
		review_rating = '4 stars'
	elif soupreview.find("p", {"class": "star-rating Three"}):
		review_rating = '3 stars'
	elif soupreview.find("p", {"class": "star-rating Two"}):
		review_rating = '2 stars'
	elif soupreview.find("p", {"class": "star-rating One"}):
		review_rating = '1 stars'
	else :
		review_rating = 'no rating'

	# extraction des éléments de la table
	tds = soup.select('td')

	UPC = tds[0]
	title = soup.find('h1')
	price_including_tax = tds[2]
	price_excluding_tax = tds[3]
	number_available = tds[5]
	
	#product description ou 'vide' si absent:
	test_product_description = soup.find('div', id='product_description')
	
	if test_product_description is None:
		product_description = ''
	else:
		product_description = soup.find('div', id='product_description').find_next('p').text
	
	#url de l'image
	img = soup.find("div", class_ = "item active").img['src']
	img = re.sub(r"../../media", "https://books.toscrape.com/media", img)

	# création du dictionnaire:

	scrap_page = {}
	scrap_page['product_page_url'] = urlpage
	scrap_page['universal_ product_code'] = UPC.text
	scrap_page['title'] = title.text
	scrap_page['price_including_tax'] = price_including_tax.text
	scrap_page['price_excluding_tax'] = price_excluding_tax.text
	scrap_page['number_available'] = number_available.text
	scrap_page['product_description'] = product_description
	scrap_page['category'] = category.text
	scrap_page['review_rating'] = review_rating
	scrap_page['image_url'] = img
	
	#Nom de fichier csv et jpg pour une seule page
	title_csv = title.text
	title_csv = re.sub('[<>:«|\/?*"]', '-', title_csv)
	title_img = title_csv+".jpg"
	title_csv = title_csv +".csv"

	return(scrap_page, title_csv, img, title_img)
	
#utilisation manuelle du script pour une page:

if __name__ == "__main__":

	#demande de saisie de l'url du livre
	urlpage = input("url page a scraper:")
	returned = scraper_page(urlpage)
	#recuperation du contenu de la page
	scrap_page = {}
	scrap_page = returned[0]

	#titre pour nommer le CSV et jpg
	title_csv = returned[1]
	title_img = returned[3]
	#création du CSV
	with open(title_csv, 'w', newline='', encoding='utf-8') as f:
		fieldnames = ['product_page_url', 'universal_ product_code', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
		thewriter = csv.DictWriter(f, fieldnames=fieldnames)
		thewriter.writeheader()
		thewriter.writerow(scrap_page)

	#demande si l'on veut garder l'image du livre puis l'enregistre si Y
	img_check = str(input("Voulez vous enregistrer l'image ? (Y/N): ")).lower().strip()
	if img_check == 'y':		
		url_img = scraper_page(urlpage)[2]
		urllib.request.urlretrieve(url_img, title_img)
		print("l'image est enregistrée sous le nom :", title_img)
	elif img_check == 'n':
		print("l'image ne sera pas enregistrée")
	else:
		print("Commande invalide: l'image ne sera pas enregistrée")
	print("le fichier est enregistré sous le nom :", str(title_csv))