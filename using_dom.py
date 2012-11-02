#Creates an xml_parser class that opens the filename that is passed
#in to the init constructor and parses the xml data contained within


import io
import urllib2
import lxml
from bs4 import BeautifulSoup
from xml.dom.minidom import parse, parseString



class xml_parser():

	def __init__(self, filename):
		open_stream = open('index.rss', 'rt')
		self.data = open_stream.read()
		return None
		

	#takes in a neighborhood and a borough parameter and hits the craigslist url
	#results are returned in the price variable.
	def find_by_hood(self, neighborhood):
		xml_soup = BeautifulSoup(self.data, 'xml')
		items = xml_soup.findAll('item')
		for x in items:
			price = '' #empty string to store the price of each item
			string = str(x.title) #find all the title tags in each craigslist item
			index = string.find('(') #find the index of an opening paren - this is where the cl neighborhood data typicall lives
			string = string[index:] #slice string up until the neighborhood and price info
			if string.find(str(neighborhood)) != -1: #if the neighborhood string is found in the title
				index = string.find('$') #find the price
				for i in range(5):
					price += (string[i + 1 + index])
				print 'this is the price: ', price, 'in this hood: ', neighborhood
				



