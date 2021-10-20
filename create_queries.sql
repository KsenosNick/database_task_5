create table if not exists Genre (
	id serial primary key,
	name varchar(50) not null unique
);

create table if not exists Artist (
	id serial primary key,
	name varchar(50) not null
);

create table if not exists ArtistGenre (
	genre_id integer references Genre(id),
	artist_id integer references Artist(id),
	constraint artist_genre_pk primary key (genre_id, artist_id)
);

create table if not exists Album (
	id serial primary key,
	title varchar(50) not null,
	year_issue integer not null
);

create table if not exists ArtistAlbum (
	album_id integer references Album(id),
	artist_id integer references Artist(id),
	constraint artist_album_pk primary key (album_id, artist_id)
);

create table if not exists Track (
	id serial primary key,
	title varchar(50) not null,
	duration integer not null,
	album_id integer not null references Album(id)
);

create table if not exists Collection (
	id serial primary key,
	title varchar(50) not null,
	year_issue integer not null
);

create table if not exists TrackCollection (
	track_id integer references Track(id),
	collection_id integer references Collection(id),
	constraint track_collection_pk primary key (track_id, collection_id)
);
