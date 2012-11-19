import sched, time, io
import urllib2
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime

#global list of neighborhood names to track
NEIGHBORHOOD_LIST = [
    'Bay Ridge',
    'Bay ridge',
    'Bed-Stuy',
    'BedStuy',
    'Bedford-Stuyvesant',
    'Bedstuy',
    'Bensonhurst',
    'Brooklyn Heights',
    'Brooklyn heights',
    'Bushwick',
    'Canarsie',
    'Carrol Gardens',
    'Carroll Gardens',
    'Carrol Garden',
    'Clinton Hill',
    'Clinton hill',
    'Crown Heights',
    'Crown heights',
    'Ditmas Park',
    'Ditmas park',
    'DUMBO',
    'East Williamsburg',
    'Fort Green', #misspelling will catch the correct one too...#megabonus
    'Greenpoint',
    'Park Slope',
    'Prospect Heights',
    'Red Hook',
    'Red hook',
    'Sunset Park',
    'Sunset park',
    'Vinegar Hill',
    'Vinegar hill',
    'Williamsburg',
]

CL_URL = 'http://newyork.craigslist.org/brk/aap/index.rss'

def run_scheduler():
    print "Running craigslist scraper..."
    parse_data(pull_data())

def pull_data(url=CL_URL):
    data = urllib2.urlopen(url)
    xml_header = '<?xml version="1.0" encoding="iso-8859-1"?>'
    return "".join(line for line in data if line.find(xml_header) == -1)

def parse_data(data):
    items = BeautifulSoup(data, 'xml').findAll('item')
    for item in items:
        description = item.description.string.rstrip()
        title = item.title.string
        index = title.rfind('(')
        if index != -1: #error check if there is no parens for the neighborhood
            br_info = title[index:] #slice the string at the opening paren
            url = item.link.string
            attrs = map(lambda f: f(br_info), [find_nabe, find_price, find_bedrooms])
            make_listing(None, url, title, description, *attrs)

def make_listing(sql_id, url, title, description, neighborhood, price, bedrooms):
    if not get_by_url(url) and neighborhood and price and bedrooms != -1:
        print "Inserting {}...".format(url)
        listing = (sql_id, url, price, bedrooms, title, description, datetime.now())
        conn.execute('INSERT INTO listing VALUES(?,?,?,?,?,?,?)', listing)
        insert_relation(url, neighborhood)

def select(conn, attr, table, **kv):
    criterion, val = kv.items()[0]
    command = "SELECT {} FROM {} WHERE {}=(?)".format(attr, table, criterion)
    return conn.execute(command, (val,))

#inserts into the relation table 'list_to_neighborhood' by finding the url
#handles the case of multiple neighborhood in the current_neighborhoods parameter
#by looping through and inserting a new relation for each one
def insert_relation(current_url, current_neighborhoods):
    listing_id = select(conn, "id", "listing", url=current_url).fetchone()
    for item in current_neighborhoods:
        neighborhood_id = select(conn, "id", "neighborhood", name=item).fetchone()
        conn.execute('INSERT INTO list_to_neighborhood VALUES(?,?)', (listing_id[0], neighborhood_id[0]))


def get_by_url(url):
    return select(conn, "*", "listing", url=url).fetchall()

#loops through nabe list to check if any appear in the item
def find_nabe(item):
    return [x for x in NEIGHBORHOOD_LIST if any(item.find(y) != -1 for y in [x, x.lower(), x.upper()])]

def find_price(item):
    price = ''
    index = item.rfind('$')
    if index != -1:
        item = item[index + 1:]
        for i in range(5):
            if i >= len(item):
                break
            elif not(item[i].isdigit()):
                break
            else:
                price += item[i]
                return price

#clumsy function that slices twice, but little alternative because of messy CL XML where the
#bedroom data isn't offset with a tag
def find_bedrooms(item):
    bedrooms = ''
    index = item.rfind('$') #rfind to find the last $
    item = item[index:]
    index = item.find('bd')
    if index != -1:
        bedrooms = item[index -1]
        return bedrooms

if __name__ == '__main__':
    conn = sqlite3.connect('housing.db')
    run_scheduler()
    conn.commit()
    conn.close()
