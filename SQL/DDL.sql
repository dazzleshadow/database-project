CREATE TABLE artist
(
	name varchar(10) not null,
	company varchar(10),
	primary key(name)
)	ENGINE=INNODB;

CREATE TABLE album
(
	name varchar(10) not null,
	year int,
	artist varchar(10),
	primary key(name),
	foreign key (artist) references artist(name)
)	ENGINE=INNODB;

CREATE TABLE series
(
	name varchar(10) not null,
	type varchar(10),
	primary key(name)
)	ENGINE=INNODB;

CREATE TABLE song
(
	ID int AUTO_INCREMENT PRIMARY KEY,
	name varchar(10) not null,
	link varchar(11),
	artist varchar(10),
	album varchar(10),
	series varchar(10),
	foreign key (artist) references artist(name),
	foreign key (album) references album(name),
	foreign key (series) references series(name)
)	ENGINE=INNODB;

CREATE TABLE playlist
(
	Sequence int AUTO_INCREMENT PRIMARY KEY,
	song_id int,
	foreign key (song_id) references song(ID)
)	ENGINE=INNODB;
