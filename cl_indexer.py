import sched, time, io
import urllib2
from bs4 import BeautifulSoup
import sqlite3
import datetime

#global list of neighborhood names to track
NEIGHBORHOOD_LIST = [
			'Bay Ridge',
			'Bay ridge',
			'Bed-Stuy',
			'BedStuy',
			'Bedford-Stuyvesant',
			'Bedstuy',
			'Bensonhurst',
			'Brooklyn Heights',
			'Brooklyn heights',
			'Bushwick',
			'Canarsie',
			'Carrol Gardens',
			'Carroll Gardens',
			'Carrol Garden',
			'Clinton Hill',
			'Clinton hill',
			'Crown Heights',
			'Crown heights'
			'Ditmas Park',
			'Ditmas park',
			'DUMBO',
			'East Williamsburg',
			'Fort Green', #misspelling will catch the correct one too...#megabonus
			'Greenpoint',
			'Park Slope',
			'Prospect Heights',
			'Red Hook',
			'Red hook',
			'Sunset Park',
			'Sunset park',
			'Vinegar Hill',
			'Vinegar hill',
			'Williamsburg',
			]

CL_URL = 'http://newyork.craigslist.org/brk/aap/index.rss'



def run_scheduler():
	x = 0
	while True:
		write_data()
		parse_data()
		print 'iteration number: ', x
		time.sleep(3600)
		x += 1

#pings the craigslist rss url, writes the data to a file
#defaulted to the cl brooklyn url
def write_data():
	data = urllib2.urlopen(CL_URL)
	with open('index.rss', 'wt') as outstream:
		for line in data:
			if line.find('<?xml version="1.0" encoding="iso-8859-1"?>') == -1:
				outstream.write(line)


def parse_data():
	with open('index.rss', 'rt') as file:
		read_string = file.read()
	items = BeautifulSoup(read_string, 'xml').findAll('item')
	for item in items:
		title = item.title.string
		index = title.rfind('(')
		if index != -1: #error check if there is no parens for the neighborhood
			title = title[index:] #slice the string at the opening paren
			url = item.link.string
			make_list(title, url)

def make_list(item, url):
	if not (get_by_url(url)):
		neighborhood = str(find_nabe(item)) #have to cast to str for db commit
		price = find_price(item)
		bedrooms = find_bedrooms(item)
		now = datetime.datetime.now()
		if (neighborhood != [] and price != [] and bedrooms != -1):
			listing = (url, neighborhood, price, bedrooms, now)
			conn.execute('INSERT INTO listings VALUES(?,?,?,?,?)', listing)

def get_by_url(url):
	return (conn.execute('SELECT * FROM listings WHERE url=(?)', (url,))).fetchall()

#loops through nabe list to check if any appear in the item
def find_nabe(item):
	return [x for x in NEIGHBORHOOD_LIST if any(item.find(y) != -1 for y in [x, x.lower(), x.upper()])]


def find_price(item):
	price = ''
	index = item.rfind('$')
	if index != -1:
		item = item[index + 1:]
		for i in range(5):
			if i >= len(item): break
			elif not(item[i].isdigit()): break
			else: 
				price += item[i]
	print 'price: ', price
	return price



def find_bedrooms(item):
	bedrooms = ''
	index = item.rfind('$') #rfind to find the last $
	item = item[index:]
	index = item.find('bd')
	if index != -1:
		bedrooms = item[index -1]
	return bedrooms



conn = sqlite3.connect('test_db.db')
cursor = conn.cursor()
run_scheduler()
conn.commit()
conn.close()



