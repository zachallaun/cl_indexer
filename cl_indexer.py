import sched, time, io
import urllib2
from using_dom import xml_parser


class fetch_cl_data():

	def __init__(self):
		pass

	#def event_scheduler(self):



	def fetch_data(self):
		data = urllib2.urlopen('http://newyork.craigslist.org/brk/aap/index.rss')



	def get_cl_data(self):
		s = sched.scheduler
		parser = xml_parser(index.rss)
