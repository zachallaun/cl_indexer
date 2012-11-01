import io
import urllib2
from bs4 import BeautifulSoup
from xml.dom.minidom import parse, parseString


class xml_parser():

	def __init__(self):
		self.items = []
		return None
		

	#takes in a neighborhood and a borough parameter and hits the craigslist url
	#results are returned in the price variable.
	def find_by_hood(self, borough, neighborhood):
		string_list = ['http://newyork.craigslist.org/', borough, '/aap/index.rss']
		url_string = ''.join(string_list)
		index = str(urllib2.urlopen(url_string).read())
		xml_soup = BeautifulSoup(index, 'xml', from_encoding="iso-8859-1")
		print xml_soup.item
		for x in xml_soup.items:
			print '\n\n\n\nin self.items loop'
			title = str(x.title)
			price = ''
			if title.find(str(neighborhood)) != -1 or title.find((str(neighborhood)).lowercase) != -1:
				index = title.find('$')
				for i in range(5):
					price += (title[i + 1 + index])
				print '\n\nThis is the price: ', price




this_parser = xml_parser()
this_parser.find_by_hood('mnh', 'village')



