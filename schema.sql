
CREATE TABLE listing (
	id integer primary key,
	url text,
	price integer,
	bedrooms integer,
	description text,
	title text,
	datetime integer
);

CREATE TABLE neighborhood (
	id INTEGER primary key,
	name text,
	keywords text
);

CREATE TABLE list_to_neighborhood (
	listing_id integer,
	neighborhood_id integer
);