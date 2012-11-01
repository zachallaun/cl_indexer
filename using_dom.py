#Creates an xml_parser class that opens the filename that is passed
#in to the init constructor and parses the xml data contained within


import io
import urllib2
from bs4 import BeautifulSoup
from xml.dom.minidom import parse, parseString


class xml_parser():

	def __init__(self, filename):
		open_stream = open('index.rss', 'rt')
		self.data = open_stream.read()
		return None
		

	#takes in a neighborhood and a borough parameter and hits the craigslist url
	#results are returned in the price variable.
	def find_by_hood(self, borough, neighborhood):
		xml_soup = BeautifulSoup(self.data, 'xml', from_encoding="iso-8859-1")
		items = xml_soup('item')	
		for x in items: #loop through the items in xml_soup
			price = '' #empty string to store the price of each item
			string = str(x.title) 
			if string.find(str(neighborhood)) != -1: #if the neighborhood string is found in the title
				print string
				index = string.find('$') #find the price
				for i in range(5):
					price += (string[i + 1 + index])
				print 'this is the price: ', price

#this_parser = xml_parser('index.rss')
#this_parser.find_by_hood('mnh', 'Williamsburg')
