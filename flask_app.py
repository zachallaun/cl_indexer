from __future__ import with_statement
from contextlib import closing
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
        abort, render_template, flash
from using_the_data import db_access

#configuration
DATABASE = 'housing.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

#create our little application
app = Flask(__name__)
app.config.from_object(__name__)

@app.before_request
def before_request():
	g.db = db_access()

@app.teardown_request
def teardown_request(exception):
	g.db.close()

@app.route('/')
def front_page():
	return render_template('layout.html')
	#show front page - map of how to get different entries

@app.route('/neighborhoods', methods = ['GET'])
def show_neighborhoods():
	
	#show a list of neighborhoods

@app.route('/bedrooms', methods = ['GET'])
def show_bedrooms():
	pass
	#show bedrooms options

@app.route('/prices', methods=['GET'])
def show_prices():
	pass
	#show price options

if __name__ == '__main__':
	app.run()

