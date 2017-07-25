#!usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import sys
import csv

reload(sys)
sys.setdefaultencoding('utf-8')

def get_html(url):
	responce = requests.get(url)
	html = responce.text
	return html

def write_csv(data):
	with open('olx1.csv', 'a') as f:
		writer = csv.writer(f)

		writer.writerow( (data['title'],
						 (data)['price'],
						  data['district'],
						  data['url_page']) )

def get_page_data(html):
	soup = BeautifulSoup(html, 'lxml')
	# title, price, district, url
	ads = soup.select("[class~=space]")
	
	for ad in ads:
		try:
			title = ads.find('h3', class_='x-large').text.strip()
		except:
			title = ''

		try:
			price = ads.find('p', class_="price").text.strip()
		except:
			price = ''

		try:
			district = ads.find('td', valign="bottom").text.strip()
		except:
			district = ''

		try:
			url_page = str(ads.find('a').get('href'))
		except:
			url_page = ''
	   
		data = {'title': title, 'price': price, 'district': district, 'url_page': url_page}
		write_csv(data)

def main():
	url = 'https://www.olx.ua/nedvizhimost/prodazha-kvartir/vtorichnyy-rynok/cherkassy/'
	base_url = 'https://www.olx.ua/nedvizhimost/prodazha-kvartir/vtorichnyy-rynok/cherkassy/'
	page_part = '?page='
	total_pages = int(5)

	for i in range(1, total_pages):
		url = base_url + page_part + str(i)
	#	https://www.olx.ua/nedvizhimost/prodazha-kvartir/vtorichnyy-rynok/cherkassy/?page=8
		print(url)
		html = get_html(url)
		print('html', html)
		get_page_data(html)
		print('Parsing %d%% ' % (i / total_pages * 100))

if __name__ == '__main__':
	main()