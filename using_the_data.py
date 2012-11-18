import sqlite3
from collections import defaultdict


DATABASE = 'housing.db'

def get_by_bedrooms(input_brs):
	return conn.execute('SELECT * FROM listing where bedrooms=(?)', (input_brs,))


def get_by_neighborhood(input_hood):
	items =  conn.execute('SELECT listing.price, listing.title, listing.bedrooms, neighborhood.name FROM listing, list_to_neighborhood, neighborhood WHERE listing.id = list_to_neighborhood.listing_id AND neighborhood.id = list_to_neighborhood.neighborhood_id AND neighborhood.name = (?)', (input_hood,)).fetchall()
	return items

def get_by_max_price(max_price):
	items= conn.execute(
		'SELECT listing.url, listing.price, neighborhood.name FROM listing, list_to_neighborhood, neighborhood WHERE listing.id = list_to_neighborhood.listing_id AND neighborhood.id = list_to_neighborhood.neighborhood_id AND listing.price<(?)', (max_price,)).fetchall()
	return items

def get_by_min_price(min_price):
	items= conn.execute(
		'SELECT listing.url, listing.price, neighborhood.name FROM listing, list_to_neighborhood, neighborhood WHERE listing.id = list_to_neighborhood.listing_id AND neighborhood.id = list_to_neighborhood.neighborhood_id AND listing.price>(?)', (min_price,)).fetchall()
	return items

#not working yet
def get_by_keyword(word):
	items = conn.execute(
		'SELECT * FROM listing where listing.description LIKE % ? %', (word,)).fetchall()
	return items

def get_price_by_neighborhood(price, input_hood):
	items =  conn.execute('SELECT listing.url, listing.price, neighborhood.name from listing, list_to_neighborhood, neighborhood WHERE listing.price < (?) AND listing.id = list_to_neighborhood.listing_id AND neighborhood.id = list_to_neighborhood.neighborhood_id AND neighborhood.name = (?)', (price, input_hood)).fetchall()
	return items

def get_br_by_neighborhood(input_brs, input_hood):
	#items = conn.execute('SELECT listing.url, listing.price, listing.bedrooms, neighborhood.name from listing, list_to_neighborhood, neighborhood WHERE listing.bedrooms = (?) AND listing.id = list_to_neighborhood.listing_id AND neighborhood.id = list_to_neighborhood.neighborhood_id AND neighborhood.name = (?)', (input_brs, input_hood)).fetchall()
	#return items

	with conn:
		#row factory selects a dictionary return value instead of tuples
		conn.row_factory = sqlite3.Row
		rows = get_by_neighborhood(input_hood)
		bedroom_dict = defaultdict(int)
		bedroom_dict = {1 : 0, 2 : 0, 3 : 0, 4 : 0, 5 : 0, 6 : 0}


def avg_price_by_hood(input_hood):
	with conn:
		#row factory selects a dictionary return value instead of tuples
		conn.row_factory = sqlite3.Row
		rows = get_by_neighborhood(input_hood)
		prices = num_listings = 0
		for row in rows:
			prices += row['price'] #can use dictionary access syntax because of row factory
			listings += 1

	print 'total: ', prices, '  # of listings: ', listings
	print '\n\naverage: ', prices/listings
	return prices, listings

def avg_bedrooms_by_hood(input_hood):
		with conn:
			#row factory selects a dictionary return value instead of tuples
			conn.row_factory = sqlite3.Row
			rows = get_by_neighborhood(input_hood)
			bedroom_dict = {1 : 0, 2 : 0, 3 : 0, 4 : 0, 5 : 0, 6 : 0}
			bedroom_list = [row['bedrooms'] for row in rows if row['bedrooms'] != '']
			for num in bedroom_list:
				bedroom_dict[num] += 1
		print bedroom_dict

def price_bedroom_by_hood(input_hood):
	with conn:
		#row factory selects a dict return value instead of tuples
		conn.row_factory = sqlite3.Row
		rows = get_by_neighborhood(input_hood)
		total = num_bedrooms = 0
		for row in rows:
			total += row['price']
			num_bedrooms += 1
	print 'total: ', total
	print 'num_listings: ', num_bedrooms
	print total/num_bedrooms, ' per bedroom in ', input_hood

conn = sqlite3.connect(DATABASE)
print 'Enter hood:'
s = raw_input('>>  ')
price_bedroom_by_hood(s)

