import datetime
from mongoengine import connect
from resources import *

def changeYear():
	for movie in Movie.objects.all():
		if movie.date.year is 1:
			movie.date = datetime.datetime(year=1980, month=1, day=1)
			movie.save()

connect('milo')
cY = changeYear()
