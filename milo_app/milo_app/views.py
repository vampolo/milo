from pyramid.view import view_config
from pyramid.renderers import get_renderer
from resources import *
from datetime import datetime
from pyramid.security import authenticated_userid
import random


@view_config(context='milo_app:resources.Root',
             renderer='templates/base.pt')
def main(request):
	rand = random.randint(0, Movie.objects().count()-10)
	right_movies = dict(movies=Movie.objects()[rand+5:rand+10], title="Top Movies")
	
	#Testing Next/Previous buttons 
	if request.GET.get('page_number') is None:
		page_number = 1
		first_page = 'true'
		movies = dict(movies=Movie.objects()[0:9].order_by('-date'), title='Last updates')
	if request.GET.get('next') == page_number:
		movies = dict(movies=Movie.objects()[(page_number)*9:(page_number)*9].order_by('-date'), title='Last updates')
		first_page = 'false'
	print first_page
	
	if request.GET.get('rec') == 'new':
		movies = dict(movies=Movie.objects()[9:18].order_by('-date'), title='Last updates')
		category = 'Recommended Movies'	
		
	elif not authenticated_userid(request):
		movies = dict(movies=Movie.objects()[0:9].order_by('-date'), title='Last updates')
		category = 'All Movies'
	else:
		movies = dict(movies=Movie.objects()[18:27].order_by('-date'), title='Last updates')
		category = 'Recommended Movies'
		right_movies['title']="More Recommendations"
	slider_movies = Movie.objects()[rand:rand+5]
	results = dict(movies=movies, slider_movies=slider_movies, right_movies=right_movies, category=category, page_number=page_number, first_page=first_page)
	return results

@view_config(name='about', context='milo_app:resources.Root',
				 renderer='templates/about.pt')
def about(request):
	return dict()

@view_config(name='categories', context='milo_app:resources.Root',
				 renderer='templates/categories.pt')
def categories(request):
	return dict()

@view_config(name='profile', context='milo_app:resources.Root',
				 renderer='templates/profile.pt')
def profile(request):
	return dict()

@view_config(context='milo_app:resources.Movie',
				 renderer='templates/movie.pt')
def movie(context, request):
	rand = random.randint(0, Movie.objects().count()-5)
	slider_movies = dict(movies=Movie.objects()[rand:rand+3], title='Related Movies')
	right_movies = dict(movies=Movie.objects()[rand+5:rand+10], title='Recommended by Friends')
	return dict(movie=context, slider_movies=slider_movies, right_movies=right_movies)
