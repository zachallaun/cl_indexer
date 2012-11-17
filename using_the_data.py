import sqlite3

DATABASE = 'housing.db'

def get_by_bedrooms(input_brs):
	return conn.execute('SELECT * FROM listing where bedrooms=(?)', (input_brs,))

def get_by_neighborhood(input_hood):
	neighborhood_id = conn.execute('SELECT id FROM neighborhood where name=(?)', (input_hood,)).fetchone()
	listing_ids = conn.execute('SELECT listing_id FROM list_to_neighborhood where neighborhood_id=(?)', (neighborhood_id[0],)).fetchall()
	for listing_id in listing_ids:
		item = conn.execute('SELECT * FROM listing where id=(?)', (listing_id[0],)).fetchall()
		print '\n\n', item

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
	items = conn.execute('SELECT listing.url, listing.price, listing.bedrooms, neighborhood.name from listing, list_to_neighborhood, neighborhood WHERE listing.bedrooms = (?) AND listing.id = list_to_neighborhood.listing_id AND neighborhood.id = list_to_neighborhood.neighborhood_id AND neighborhood.name = (?)', (input_brs, input_hood)).fetchall()
	for item in items:
		print '\n\n', item
		
conn = sqlite3.connect(DATABASE)
print 'Enter brs:'
price = raw_input('>>  ')
print '\nEnter neighborhood: '
hood = raw_input('>> ')
get_br_by_neighborhood(price, hood)