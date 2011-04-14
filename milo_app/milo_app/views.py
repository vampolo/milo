from resources import *
from datetime import datetime

def my_view(request):
	a = Movie(title='test', date=datetime.today())
	a.save()
	print a
	for i in  Movie.objects.all():
		print i 	
	return {'project':'milo_app'}
