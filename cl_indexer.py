import sched, time, io
import urllib2
from bs4 import BeautifulSoup
import sqlite3
import datetime

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
    x = 0
    write_data()
    parse_data()
    print 'iteration number: ', x
    x += 1

#pings the craigslist rss url, writes the data to a file
#defaulted to the cl brooklyn url
def write_data():
    data = urllib2.urlopen(CL_URL)
    with open('index.rss', 'wt') as outstream:
        for line in data:
            if line.find('<?xml version="1.0" encoding="iso-8859-1"?>') == -1:
                outstream.write(line)


def parse_data():
    with open('index.rss', 'rt') as file:
        read_string = file.read()
        items = BeautifulSoup(read_string, 'xml').findAll('item')
        for item in items:
            description = item.description.string
            description = description.rstrip()
            title = item.title.string
            index = title.rfind('(')
            if index != -1: #error check if there is no parens for the neighborhood
                br_info = title[index:] #slice the string at the opening paren
                url = item.link.string
                make_list(br_info, url, title, description)


def make_list(item, url, title, description):
    if not (get_by_url(url)): #if the url doesn't exists in the db, we go forward
        sql_id = None
        neighborhood = (find_nabe(item)) #have to cast to str for db commit
        price = find_price(item)
        bedrooms = find_bedrooms(item)
        now = datetime.datetime.now()
        if (neighborhood != [] and price != [] and bedrooms != -1): #tossing incomplete data
            print 'oh gosh inserting!'
            listing = (sql_id, url, price, bedrooms, title, description, now)
            conn.execute('INSERT INTO listing VALUES(?,?,?,?,?,?,?)', listing)
            insert_relation(url, neighborhood)

#inserts into the relation table 'list_to_neighborhood' by finding the url
#handles the case of multiple neighborhood in the current_neighborhoods parameter
#by looping through and inserting a new relation for each one
def insert_relation(current_url, current_neighborhoods):
    listing_id = conn.execute('SELECT id from listing where url=(?)',(current_url,)).fetchone() #returns a tuple
    for item in current_neighborhoods:
        neighborhood_id = conn.execute('SELECT id from neighborhood where name =(?)',(item,)).fetchone() # also returns a one item tuple
        conn.execute('INSERT INTO list_to_neighborhood VALUES(?,?)', (listing_id[0], neighborhood_id[0]))

def get_by_url(url):
    return (conn.execute('SELECT * FROM listing WHERE url=(?)', (url,))).fetchall()

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



