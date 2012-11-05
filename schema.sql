drop table if exists entries;
create table entries (
	id integer primary key autoincrement,
	bedrooms integer not null,
	price integer not null,
	neighborhood string not null,
	url string not null,
	date integer not null
);