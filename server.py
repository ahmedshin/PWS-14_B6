from bottle import run
from bottle import route
from bottle import request
from bottle import HTTPError

import album

@route("/hello/")
def print_hello():
	return "Hello"

@route("/albums/<artist>")
def albums(artist):
	albums_list = album.find(artist)
	sum_ = len(albums_list)
	kolich = None
	if not albums_list:
		message = "Альбом {} не найден".format(artist)
		result =  HTTPError(404, message)
	else:
		album_name = [album.album for album in albums_list]
		kolich = "Общее количество aльбомов {} - {}<br>".format(artist, sum_)
		result = "Список альбомов {}<br>".format(artist)
		result += "<br>".join(album_name)
	return kolich, result 

@route("/albums", method = "POST")
def create_artist():
    year = request.forms.get("year")
    artist = request.forms.get("artist")
    genre = request.forms.get("genre")
    album_name = request.forms.get("album")

    try:
    	year = int(year)
    except ValueError:
    	return HTTPError(400, "Неверная дата")
    try:
    	new_artist = album.save_artist(year, artist, genre, album_name)		
    except AssertionError as err:
    	result = HTTPError(400, str(err))
    except album.AlreadyExists as err:
    	result = HTTPError(409, str(err))
    else:
    	print("Новый исполнитель - {} сохранен:".format(new_artist.id))
    	result = "Альбом #{} успешно сохранен".format(new_artist.id)
    return result

if __name__ == '__main__':
	run(host = "localhost", port = 8080, debug = True )