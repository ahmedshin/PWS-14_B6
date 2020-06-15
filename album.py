import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()


class Error(Exception):
    pass


class AlreadyExists(Error):
    pass

class Album(Base):
	__tablename__ = "album"

	id = sa.Column(sa.INTEGER, primary_key = True)
	year = sa.Column(sa.INTEGER)
	artist = sa.Column(sa.TEXT)
	genre = sa.Column(sa.TEXT)
	album = sa.Column(sa.TEXT)

def connect_db():
	
	engine = sa.create_engine(DB_PATH)
	Base.metadata.create_all(engine)
	session = sessionmaker(engine)
	return session()

def find(artist):
	session = connect_db()
	albums = session.query(Album).filter(Album.artist == artist).all()
	return albums

def save_artist(year, artist, genre, album):
	assert isinstance(year, int), "Неверная дата"
    

	session = connect_db()
	find_artist = session.query(Album).filter(Album.artist == artist).first()

	if find_artist is not None:
		raise AlreadyExists("Такой исполнитель уже существует #{}".format(find_artist.id))

	# saved_album = session.query(Album).filter(Album.artist == artist).first()
 #    if saved_album is not None:
 #        raise AlreadyExists("Album already exists and has #{}".format(saved_album.id))


	groupe = Album(year = year, artist=artist, genre=genre, album=album)
	
	session.add(groupe)
	session.commit()
	return groupe