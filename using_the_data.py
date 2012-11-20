
import sqlite3
from collections import defaultdict


def sqlstr(command, verbose=False):
    return command.replace("\n", " ") if verbose else command

class db_access():

    def __init__(self, db_name='housing.db'):
        self.conn = sqlite3.connect(db_name)

    def get_by_bedrooms(self, input_brs):
        command = sqlstr('SELECT * FROM listing where bedrooms=(?)', True)
        return self.conn.execute(command, (input_brs,)).fetchall()

    def get_by_neighborhood(self, input_hood):
        command = sqlstr("""SELECT listing.price, listing.title,
                                   listing.bedrooms, neighborhood.name
                            FROM listing, list_to_neighborhood, neighborhood
                            WHERE listing.id = list_to_neighborhood.listing_id
                            AND neighborhood.id = list_to_neighborhood.neighborhood_id
                            AND neighborhood.name = (?)""", True)
        items = self.conn.execute(command, (input_hood,)).fetchall()
        return items

    def get_by_max_price(self, max_price):
        command = sqlstr("""SELECT listing.url, listing.price,
                                   neighborhood.name
                            FROM listing, list_to_neighborhood, neighborhood
                            WHERE listing.id = list_to_neighborhood.listing_id
                            AND neighborhood.id = list_to_neighborhood.neighborhood_id
                            AND listing.price<(?)""", True)
        items = self.conn.execute(command, (max_price,)).fetchall()
        return items

    def get_by_min_price(self, min_price):
        command = sqlstr("""SELECT listing.url, listing.price, neighborhood.name
                            FROM listing, list_to_neighborhood, neighborhood
                            WHERE listing.id = list_to_neighborhood.listing_id
                            AND neighborhood.id = list_to_neighborhood.neighborhood_id
                            AND listing.price>(?)""")
        items = self.conn.execute(command, (min_price,)).fetchall()
        return items

    #not working yet
    def get_by_keyword(self, word):
        items = self.conn.execute('SELECT * FROM listing where listing.description LIKE % ? %', (word,)).fetchall()
        return items

    def get_price_by_neighborhood(self, price, input_hood):
        command = sqlstr("""SELECT listing.url, listing.price, neighborhood.name
                            FROM listing, list_to_neighborhood, neighborhood
                            WHERE listing.price < (?)
                            AND listing.id = list_to_neighborhood.listing_id
                            AND neighborhood.id = list_to_neighborhood.neighborhood_id
                            AND neighborhood.name = (?)""")
        items = self.conn.execute(command, (price, input_hood)).fetchall()
        return items

    def get_br_by_neighborhood(self, input_brs, input_hood):
        #items = conn.execute('SELECT listing.url, listing.price, listing.bedrooms, neighborhood.name from listing, list_to_neighborhood, neighborhood WHERE listing.bedrooms = (?) AND listing.id = list_to_neighborhood.listing_id AND neighborhood.id = list_to_neighborhood.neighborhood_id AND neighborhood.name = (?)', (input_brs, input_hood)).fetchall()
        #return items
        with self.conn:
            #row factory selects a dictionary return value instead of tuples
            self.conn.row_factory = sqlite3.Row
            rows = self.get_by_neighborhood(input_hood)
            bedroom_dict = defaultdict(int)
            bedroom_dict = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

    def avg_price_by_hood(self, input_hood):
        with self.conn:
            #row factory selects a dictionary return value instead of tuples
            self.conn.row_factory = sqlite3.Row
            rows = self.get_by_neighborhood(input_hood)
            prices = num_listings = 0
            for row in rows:
                prices += row['price'] #can use dictionary access syntax because of row factory
                num_listings += 1
        avg = prices / num_listings
        return prices, num_listings, avg

    def avg_bedrooms_by_hood(self, input_hood):
        with self.conn:
            #row factory selects a dictionary return value instead of tuples
            self.conn.row_factory = sqlite3.Row
            rows = self.get_by_neighborhood(input_hood)
            bedroom_dict = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
            bedroom_list = [row['bedrooms'] for row in rows if row['bedrooms'] != '']
            for num in bedroom_list:
                bedroom_dict[num] += 1
        return bedroom_dict

    def price_bedroom_by_hood(self, input_hood):
        with self.conn:
            #row factory selects a dict return value instead of tuples
            self.conn.row_factory = sqlite3.Row
            rows = self.get_by_neighborhood(input_hood)
            total = num_bedrooms = 0
            for row in rows:
                if row['bedrooms'] != '':
                    total += row['price']
                    num_bedrooms += int(row['bedrooms'])
                    return total / num_bedrooms, input_hood

    def close(self):
        self.conn.close()
