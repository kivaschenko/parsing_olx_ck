#!usr/bin/env python3
#	to contact: teodorathome@yahoo.com

import requests
from bs4 import BeautifulSoup
import sys
import csv
from time import sleep

reload(sys)
sys.setdefaultencoding('utf-8')

def get_html(url):
	responce = requests.get(url)
	#	Get all html from current page: html
	html = responce.text
	return html

def save(ad, path):
	"""  The function to write data set in csv-file by chunk from function "get_page_links" """
	#	To write data using the metode 'a' that make next item at the end
	with open(path, 'a') as f:
		writer = csv.writer(f)
		writer.writerow((ad['title'], ad['price'], ad['link']))

def get_page_links(html):
	#	Get the html page: html_soup
	html_soup = BeautifulSoup(html, 'lxml')
	#	Get all links ads from current page by CSS selector "Find tags by CSS class": all_links
	all_links = html_soup.select(".marginright5")
	#	Get all titles of ads from current page in list: title
	title = [item.text.strip() for item in all_links]
	#	Get all url-links of ads from current page in list that push into the ads page: title
	link = [x.get('href') for x in all_links]
	#	Get all prices of ads from current page by CSS selector "Find tags by CSS class": all_prices
	all_prices = html_soup.select(".price")
	#	Get the all prices in object format and added in list: price
	price = [p.text.strip() for p in all_prices[2:]]
	#	Made the list of tuples including the elements of previos names by zip module: ads
	all_values = list(zip(title, price, link))
	#	We will make a dictionary from the values of the list of tuples bypassing them in turn:
	for tuple3 in all_values:
		ad = {'title': tuple3[0], 'price': tuple3[1], 'link': tuple3[2]}
		#	Pass to function "save"
		save(ad, 'ads5.csv')


def main():
	""" The main function to Parsing  """
	#	This main url to first input to site and to compilate next urls to go to next pages: url
	url = 'https://www.olx.ua/nedvizhimost/prodazha-kvartir/vtorichnyy-rynok/cherkassy/'
	#	base_url = 'https://www.olx.ua/nedvizhimost/prodazha-kvartir/vtorichnyy-rynok/cherkassy/'
	#	The part of url to concatenate that contains the page atribut: page_part
	page_part = '?page='
	#	The total number of web-scraping pages : total_pages
	total_pages = int(37)

	for i in range(9, total_pages):
		url_gen = url + page_part + str(i)
		html = get_html(url_gen)
		#	Wait for answer server few second to less weighting 
		sleep(2)
		#	This function does next loop of parsing
		get_page_links(html)

if __name__ == '__main__':
	main()