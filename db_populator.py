#this program just populates the neighborhood table in the database with the 
#list of neighborhoods that we are searching for

import sqlite3

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
			'dumbo',
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


if __name__=='__main__':
	conn = sqlite3.connect('housing.db')
	keywords = ''
	this_id = None
	for name in NEIGHBORHOOD_LIST:
		conn.execute('INSERT INTO neighborhood VALUES(?,?,?)', (this_id,name, keywords))
	conn.commit()
	conn.close()
