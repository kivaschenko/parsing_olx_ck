#!usr/bin/env python3
#   to contact: teodorathome@yahoo.com

import pandas as pd 
import requests
from bs4 import BeautifulSoup
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


path = 'ads5.csv'
names = ['title', 'price', 'link']
df1 = pd.read_csv(path, header=None, names=names, encoding='utf-8')
print(df1.head())
url_list = df1['link']


def get_ads_details(url):
	responce = requests.get(url)
	html = responce.text
	soup = BeautifulSoup(html, 'lxml')
	#   Get the ads title: title
	try:
		title = soup.title.text.split(':')[0]                   
	except:
		title = ''
	#   Get the url address without label: clear_url
	try:
		clear_url = soup.find('link', rel="canonical").get('href')
	except:
		clear_url = clear_url

	#   Get price USD  from title of head html: price_usd
	try:
		price_usd = price_usd = soup.select(".price-label")
		price_usd = int(price_usd[0].text.strip().replace(' ','').replace('$',''))
	except:
		price_usd = ''  
	#   Get the text of ads: text_content
	try:
		text_content = soup.select("#textContent")
		text_content = text_content[0].text.strip()[:200]           
	except:
		text_content = ''


	#   Get the flat values ads: values
	values = soup.select(".value")

	try:
		seller = values[0].text.strip() 
	except:
		seller = ''
	try:
		market = values[1].text.strip()
	except:
		market = ''             
	try:
		rooms = values[2].text.strip()
	except:
		rooms = ''              
	try:
		total_area = values[3].text.strip()
		total_area = int(total_area.split(' ')[0])
	except:
		total_area = ''
	try:
		live_area = values[4].text.strip()
	except:
		live_area = ''          
	try:
		kitchen_area = values[5].text.strip()
	except:
		kitchen_area = ''
	try:
		walls = values[6].text.strip()
	except:
		walls = ''
	try:
		floor = values[7].text.strip()
	except:
		floor = ''
	try:
		floors = values[8].text.strip()
	except:
		floors = ''   

	if type(price_usd) and type(total_area) == 'int':
		price_sqr = round(price_usd / total_area)
	else:
		price_sqr = ''

	flck = {'price_usd'   : price_usd,
			'seller'      : seller,
			'market'      : market,
			'rooms'       : rooms,
			'total_area'  : total_area,
			'live_area'   : live_area,
			'kitchen_area': kitchen_area,
			'walls'       : walls,         
			'floor'       : floor,
			'floors'      : floors,
			'title'       : title,
			'text_content': text_content,
			'clear_url'   : clear_url,
			'price_sqr'   : price_sqr }
	save(flck, 'flat_3.csv')

def save(flat, path_write):
	with open(path_write, 'a') as f:
		writer = csv.writer(f) 
		writer.writerow(   (flat['rooms'],
							flat['price_usd'],
							flat['price_sqr'],             
							flat['total_area'],
							flat['live_area'],
							flat['kitchen_area'],
							flat['walls'],         
							flat['floor'],
							flat['floors'],
							flat['seller'],
							flat['market'],
							flat['title'],
							flat['text_content'],
							flat['clear_url'])   )

def main():
	for url in url_list:
		get_ads_details(url)

if __name__ == '__main__':
	main()