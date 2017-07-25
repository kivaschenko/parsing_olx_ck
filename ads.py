#!usr/bin/env python3
#	teodorathome@yahoo.com

import requests
from bs4 import BeautifulSoup
import sys
import csv
# from time import sleep

# reload(sys)
# sys.setdefaultencoding('utf-8')

def get_html(url):
	responce = requests.get(url)
	html = responce.text
	return html

def save(ads_list, path):
	with open(path, 'a') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow((ads_list[0], ads_list[1], ads_list[2]))

def get_page_links(html):
	html_soup = BeautifulSoup(html, 'lxml')
	ads = list(('Title', 'Price', 'Link'))
	all_links = html_soup.select(".marginright5")
	title = [item.text.strip() for item in all_links]
	link = [x.get('href') for x in all_links]
	all_prices = html_soup.select(".price")
	price = [p.text.strip() for p in all_prices[2:]]
	ads = list(zip(title, price, link))
	save(ads, 'ads.csv')


def main():
	url = 'https://www.olx.ua/nedvizhimost/prodazha-kvartir/vtorichnyy-rynok/cherkassy/'
	base_url = 'https://www.olx.ua/nedvizhimost/prodazha-kvartir/vtorichnyy-rynok/cherkassy/'
	page_part = '?page='
	total_pages = int(7)

	for i in range(1, total_pages):
		url = base_url + page_part + str(i)
	#	https://www.olx.ua/nedvizhimost/prodazha-kvartir/vtorichnyy-rynok/cherkassy/?page=8
		print('Parsing %d%% ' % float((i / 0.37)))
		html = get_html(url)
		#sleep(3)
		get_page_links(html)

if __name__ == '__main__':
	main()