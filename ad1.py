#!usr/bin/env python3
#	to contact: teodorathome@yahoo.com

import pandas as pd 
import requests
from bs4 import BeautifulSoup
import sys
import csv
#	from time import sleep

reload(sys)
sys.setdefaultencoding('utf-8')


path = 'ads5.csv'
names = ['title', 'price', 'link']
df1 = pd.read_csv(path, header=None, names=names, encoding='utf-8')
df1 = df1.sort_values(by='price', ascending=False)
print(df1.head())
url_list = df1['link']


def get_ads_details(url):
	responce = requests.get(url)
	html = responce.text
	soup = BeautifulSoup(html, 'lxml')
	
	#	Get the ads title: title
	try:
		title = soup.title.text.split(':')[0]					
	except:
		title = ''
	
	#	Get price USD  from title of head html: price_usd
	try:
		price_usd = soup.title.text.split(':')[1].split('$')[0].strip()
		price_usd = int(price_usd.replace(' ', ''))	
	except:
		price_usd = ''			
	
	#	Get the flat values ads: values
		values = soup.find_all('td', class_="value")
	
	#	Get the seller type: seller
	try:
		seller = values[0].text.strip()
	#	.split('\t')[-1]	
	except:
		seller = ''
					
	#	Get the the market segment: market
	try:
		market = values[1].text.strip()
	#	.split('\t')[-1]
	except:
		market = ''				

	#	Get the rooms number: rooms
	try:
		rooms = values[2].text.strip()
	#	.split('\t')[-1]
	except:
		rooms = ''				
	
	#	Get the value of total area of flat: total_area
	try:
		total_area = values[3].text.strip()
	#	.split('\t')[-1]
	#	total_area = int(total_area.split(' ')[0])
	except:
		total_area = ''
							
	#	Count the price per sqr: price_per_sqr
	# try:
	# 	price_per_sqr = round(price_usd / total_area)	
	# except:
	# 	price_per_sqr = ''
					
	#	Get the live area: live_area
	try:
		live_area = values[4].text.strip()
	#	.split('\t')[-1]
	except:
		live_area = ''			
	
	#	Get the kitchen area: kitchen
	try:
		kitchen_area = values[5].text.strip()
	#	.split('\t')[-1]
	except:
		kitchen_area = ''
				
	#	Get the floor: floor
	try:
		floor = values[6].text.strip()
	#	.split('\t')[-1]	
	except:
		floor = ''
				
	#	Get floors number: floors
	try:
		floors = values[7].text.strip()
	#	.split('\t')[-1]	
	except:
		floors = ''			

	#	Get the text of ads: text_content
	try:
		text_content = soup.select("#textContent")
		text_content = text_content[0].text.strip()[:200]			
	except:
		text_content = ''

	#	Get the url address without label: clear_url
	try:
		clear_url = soup.find('link', rel="canonical").get('href')
	except:
		clear_url = clear_url

	ad2 = { 'title': title,
			'price_usd': price_usd,
			'seller': seller,
			'market': market,
			'rooms': rooms,
			'total_area': total_area,
			'live_area': live_area,
			'kitchen_area': kitchen_area,
			'floor': floor,
			'floors': floors,
			'text_content': text_content,
			'clear_url': clear_url
			}
	save(ad2, 'ads5_4.csv')


def save(ad, path_write):
	with open(path_write, 'a') as f:
		writer = csv.writer(f) 
		writer.writerow((ad['rooms'],
						 ad['price_usd'],
						 ad['total_area'],
						 ad['live_area'],
						 ad['kitchen_area'],
						 ad['floor'],
						 ad['floors'],
						 ad['market'],
						 ad['seller'],
						 ad['title'], 
						 ad['clear_url'],
						 ad['text_content'] ))

def main():
	for url in url_list:
	#	sleep(2)
		get_ads_details(url)

if __name__ == '__main__':
	main()