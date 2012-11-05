import sched, time, io
import urllib2
from bs4 import BeautifulSoup
#global list of neighborhood names to track
NEIGHBORHOOD_LIST = [
			'Williamsburg',
			'Bushwick',
			'Greenpoint',
			'Park Slope',
			'Fort Green', #misspelling will catch the correct one too...#megabonus
			'Prospect Heights',
			'Crown Heights',
			'Clinton Hill',
			'DUMBO',
			'Bed-Stuy',
			'BedStuy',
			'Bedford-Stuyvesant',
			'Bensonhurst',
			'Canarsie',
			'Red Hook',
			]


class fetch_cl_data():

	def __init__(self):
		pass

	#def event_scheduler(self):

	#pings the craigslist rss url, writes the data to a file
	#defaulted to the cl brooklyn url
	def write_data(self):
		data = urllib2.urlopen('http://newyork.craigslist.org/brk/aap/index.rss')
		outstream = open('index.rss', 'wt')
		for line in data:
			if line.find('<?xml version="1.0" encoding="iso-8859-1"?>') != -1:
				pass
			else :
				outstream.write(line)



	def get_cl_data(self):
		in_stream = open('index.rss', 'rt').read()
		items = BeautifulSoup(in_stream, 'xml').findAll('item')
		for listing in items:
			title = str(listing.title)
			index = title.find('(')
			if index == -1: break #error check if there is no parens for the neighborhood
			title = title[index:] #slice the string at the opening paren
			url = listing.link.string
			list_for_item = self.make_list(title, url)

	def make_list(self, item, url):
		list_for_item = []
		list_for_item.append(url)
		list_for_item.append(self.find_nabe(item))
		list_for_item.append(self.find_price(item))
		list_for_item.append(self.find_bedrooms(item))
		print list_for_item

	#loops through nabe list to check if any appear in the item
	def find_nabe(self, string):
		neighborhoods_in_item = []
		for neighborhood in NEIGHBORHOOD_LIST:
			if string.find(neighborhood) != -1 or string.find(neighborhood.lower()) != -1:
				neighborhoods_in_item.append(neighborhood)
		return neighborhoods_in_item

	def find_price(self, string):
		price = ''
		index = string.find('$')
		string = string[index:]
		for i in range(4):
			if string[i].isdigit():
				price += (string[i])
		return price



	def find_bedrooms(self, string):
		bedrooms = ''
		index = string.find('$')
		string = string[index:]
		index = string.find('bd')
		if index != -1:
			bedrooms = string[index -1]
		return bedrooms





tester = fetch_cl_data()
tester.write_data()
tester.get_cl_data()