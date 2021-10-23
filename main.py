import sqlalchemy
from config import host, user, password, db_name, port

try:
    db = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()
    print('Successfully connected...')
    try:
        print(f'1. Количество исполнителей в каждом жанре: \n',
        connection.execute("""
            SELECT ag.genre_id, g.name, COUNT(distinct ag.artist_id) FROM artistgenre ag
                JOIN genre g ON ag.genre_id = g.id
                GROUP BY genre_id, g.name;
                    """).fetchall(), '\n')
        print(f'2. Количество треков, вошедших в альбомы 2019-2020 годов: \n',
        connection.execute("""
            SELECT COUNT(*) FROM track
                JOIN album ON track.album_id = album.id
                WHERE year_issue BETWEEN 2019 AND 2020;
        """).fetchall(), '\n')
        print(f'3. Средняя продолжительность треков по каждому альбому: \n',
        connection.execute("""
            SELECT AVG(duration) FROM track
	            GROUP BY album_id;
        """).fetchall(), '\n')
        print(f'Все исполнители, которые не выпустили альбомы в 2020 году: \n',
        connection.execute("""
            SELECT a.name FROM artist a
                WHERE a.id NOT IN (select 
                    ar.id FROM artist ar
                    JOIN artistalbum aa ON ar.id = aa.artist_id 
                    JOIN album al ON aa.album_id = al.id
                    WHERE al.year_issue = 2020);  
        """).fetchall(), '\n')
        print(f'Названия сборников, в которых присутствует Secret garden: \n',
        connection.execute("""
            SELECT c.title FROM collection c 
                JOIN trackcollection tc ON c.id = tc.collection_id 
                JOIN track t ON tc.track_id = t.id
                JOIN album a ON t.album_id = a.id 
                JOIN artistalbum aa ON a.id = aa.album_id 
                JOIN artist ON aa.artist_id = artist.id
                WHERE artist.name LIKE 'Secret garden';
        """).fetchall(), '\n')
        print(f'Название альбомов, в которых присутствуют исполнители более 1 жанра: \n',
        connection.execute("""
            SELECT a.title, COUNT(ag.genre_id) FROM album a
                JOIN artistalbum aa ON a.id = aa.artist_id 
                JOIN artist ON aa.artist_id = artist.id 
                JOIN artistgenre ag ON artist.id = ag.artist_id 
                GROUP BY a.title
                HAVING COUNT(ag.genre_id) > 1;
        """).fetchall(), '\n')
        print(f'7. Наименование треков, которые не входят в сборники: \n',
        connection.execute("""
            SELECT title FROM track t 
                LEFT JOIN trackcollection tc ON t.id = tc.track_id 
                WHERE tc.track_id IS NULL;
        """).fetchall(), '\n')
        print(f'8. Мсполнителя(-ей), написавшего самый короткий по продолжительности трек: \n',
        connection.execute("""
            SELECT name FROM artist a
                JOIN artistalbum aa ON a.id = aa.artist_id 
                JOIN album ON aa.album_id = album.id 
                JOIN track ON album.id = track.album_id 
                WHERE duration = (select min(duration) FROM track);
        """).fetchall(), '\n')
        print(f'9. Название альбомов, содержащих наименьшее количество треков: \n',
        connection.execute("""
            SELECT a.title, COUNT(t.id) FROM album a
                JOIN track t ON a.id = t.album_id
                GROUP BY a.title
                HAVING COUNT(t.id) = (
                    SELECT COUNT(t.id) FROM album a
                        JOIN track t ON a.id = t.album_id
                        GROUP BY a.title 
                        ORDER BY count(t.id)
                        LIMIT 1
                        );
        """).fetchall(), '\n')

    finally:
        connection.close()
except Exception as ex:
    print('Connection refused...')
    print(ex)


