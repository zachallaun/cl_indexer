
import sqlite3
from collections import defaultdict


def sqlstr(command, verbose=False):
    return command.replace("\n", " ") if verbose else command

def query(command_fn):
    """Decorator. Returns a function to execute a query on a database.
    Expects command_fn to return a query string."""
    def run_query(self, *args):
        return self.conn.execute(command_fn(self), args).fetchall()
    return run_query

class QueryEngine():

    def __init__(self, db_name='housing.db'):
        self.conn = sqlite3.connect(db_name)

    @query
    def get_by_bedrooms(self):
        "Expects a number of bedrooms."
        return sqlstr('SELECT * FROM listing where bedrooms=(?)', True)

    @query
    def get_by_neighborhood(self):
        "Expects a neighborhood name."
        return sqlstr("""SELECT listing.price, listing.title,
                                listing.bedrooms, neighborhood.name
                         FROM listing, list_to_neighborhood, neighborhood
                         WHERE listing.id = list_to_neighborhood.listing_id
                         AND neighborhood.id = list_to_neighborhood.neighborhood_id
                         AND neighborhood.name = (?)""", True)

    @query
    def get_by_max_price(self):
        "Expects a max listing price."
        return sqlstr("""SELECT listing.url, listing.price,
                                neighborhood.name
                         FROM listing, list_to_neighborhood, neighborhood
                         WHERE listing.id = list_to_neighborhood.listing_id
                         AND neighborhood.id = list_to_neighborhood.neighborhood_id
                         AND listing.price<(?)""", True)

    @query
    def get_by_min_price(self):
        "Expects a min listing price."
        return sqlstr("""SELECT listing.url, listing.price, neighborhood.name
                         FROM listing, list_to_neighborhood, neighborhood
                         WHERE listing.id = list_to_neighborhood.listing_id
                         AND neighborhood.id = list_to_neighborhood.neighborhood_id
                         AND listing.price>(?)""", True)

    #not working yet
    @query
    def get_by_keyword(self):
        "Expects a keyword."
        return sqlstr('SELECT * FROM listing where listing.description LIKE % ? %')

    @query
    def get_price_by_neighborhood(self):
        "Expects a max listing price and neighborhood name."
        return sqlstr("""SELECT listing.url, listing.price, neighborhood.name
                         FROM listing, list_to_neighborhood, neighborhood
                         WHERE listing.price < (?)
                         AND listing.id = list_to_neighborhood.listing_id
                         AND neighborhood.id = list_to_neighborhood.neighborhood_id
                         AND neighborhood.name = (?)""", True)

    def get_br_by_neighborhood(self, input_brs, input_hood):
        with self.conn:
            self.conn.row_factory = sqlite3.Row
            rows = self.get_by_neighborhood(input_hood)
            bedroom_dict = defaultdict(int)
            bedroom_dict = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

    def avg_price_by_hood(self, input_hood):
        with self.conn:
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
            self.conn.row_factory = sqlite3.Row
            rows = self.get_by_neighborhood(input_hood)
            bedroom_dict = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
            bedroom_list = [row['bedrooms'] for row in rows if row['bedrooms'] != '']
            for num in bedroom_list:
                bedroom_dict[num] += 1
        return bedroom_dict

    def price_bedroom_by_hood(self, input_hood):
        with self.conn:
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
