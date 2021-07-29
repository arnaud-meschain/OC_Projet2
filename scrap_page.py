import urllib.request
from bs4 import BeautifulSoup
import re

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
	
	return(scrap_page)