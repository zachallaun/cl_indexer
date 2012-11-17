import sqlite3

DATABASE = 'housing.db'

def get_by_bedrooms(user_input):
	return conn.execute('SELECT * FROM listing where bedrooms=(?)', (user_input,))

def get_by_neighborhood(user_input):
	neighborhood_id = conn.execute('SELECT id FROM neighborhood where name=(?)', (user_input,)).fetchone()
	listing_ids = conn.execute('SELECT listing_id FROM list_to_neighborhood where neighborhood_id=(?)', (neighborhood_id[0],)).fetchall()
	for listing_id in listing_ids:
		item = conn.execute('SELECT * FROM listing where id=(?)', (listing_id[0],)).fetchall()
		print '\n\n', item

def get_by_max_price(max_price):
	items= conn.execute(
		'SELECT listing.url, listing.price, neighborhood.name FROM listing, list_to_neighborhood, neighborhood WHERE listing.id = list_to_neighborhood.listing_id AND neighborhood.id = list_to_neighborhood.neighborhood_id AND listing.price<(?)', (max_price,)).fetchall()
	for item in items:
		print '\n\n', item

def get_by_min_price(min_price):
	items= conn.execute(
		'SELECT listing.url, listing.price, neighborhood.name FROM listing, list_to_neighborhood, neighborhood WHERE listing.id = list_to_neighborhood.listing_id AND neighborhood.id = list_to_neighborhood.neighborhood_id AND listing.price>(?)', (min_price,)).fetchall()
	for item in items:
		print '\n\n', item

#not working yet
def get_by_keyword(word):
	items = conn.execute(
		'SELECT * FROM listing where listing.description LIKE % ? %', (word,)).fetchall()
	print items
	for item in items:
		print '\n\n', item

conn = sqlite3.connect(DATABASE)
print 'Enter minimum price:'
s = raw_input('>>  ')
value = get_by_min_price(s)
