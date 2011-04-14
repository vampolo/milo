from resources import *
from datetime import datetime

def my_view(request):
	'''
	ws = Ws()
	print ws.client
	print Movie.objects.all()
	'''
	a = User(email='test', password='test')
	a.save()
	return {'project':'milo_app'}
