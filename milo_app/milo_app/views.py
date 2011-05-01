from pyramid.view import view_config
from pyramid.renderers import get_renderer
from resources import *
from datetime import datetime
from pyramid.security import authenticated_userid
import random


@view_config(context='milo_app:resources.Root',
             renderer='templates/base.pt')
def main(request):
	#use 0-20 for not logged in and 20: for logged in
	if request.GET.get('rec') == 'new':
		movies = dict(movies=Movie.objects()[9:18].order_by('-date'), title='Last updates')
		category = 'Recommended Movies'
	elif not authenticated_userid(request):
		movies = dict(movies=Movie.objects()[0:9].order_by('-date'), title='Last updates')
		category = 'All Movies'
	else:
		movies = dict(movies=Movie.objects()[18:27].order_by('-date'), title='Last updates')
		category = 'Recommended Movies'
		#put right_movies here
	rand = random.uniform(0, Movie.objects().count())
	slider_movies = Movie.objects()[rand:rand+5]
	right_movies = dict(movies=Movie.objects()[rand+5:rand+10], title="Top Movies")
	return dict(movies=movies, slider_movies=slider_movies, right_movies=right_movies, category=category)

@view_config(name='about', context='milo_app:resources.Root',
				 renderer='templates/about.pt')
def about(request):
	return dict()

@view_config(name='categories', context='milo_app:resources.Root',
				 renderer='templates/categories.pt')
def categories(request):
	return dict()

@view_config(context='milo_app:resources.Movie',
				 renderer='templates/movie.pt')
def movie(context, request):
	return dict(movie=context)
