import sched, time, io
import urllib2
from using_dom import xml_parser

#global list of neighborhood names to track
nabe_list = [
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
			]



class fetch_cl_data():

	def __init__(self):
		pass

	#def event_scheduler(self):

	#pings the craigslist rss url, writes the data to a file
	#defaulted to the cl brooklyn url
	def write_data(self):
		self.data = urllib2.urlopen('http://newyork.craigslist.org/brk/aap/index.rss')
		outstream = open('index.rss', 'wt')
		for line in self.data:
			if line.find('<?xml version="1.0" encoding="iso-8859-1"?>') != -1:
				pass
			else :
				outstream.write(line)



	def get_cl_data(self):
		s = sched.scheduler
		parser = xml_parser('index.rss')
		for item in nabe_list:
			parser.find_by_hood(item)

tester = fetch_cl_data()
tester.write_data()
tester.get_cl_data()