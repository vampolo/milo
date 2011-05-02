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
	new_rec = None
	slider_movies = None
	right_movies = dict(movies=Movie.objects()[rand+5:rand+10], title="Top Movies")
	
	#Testing Next/Previous buttons
	page = request.GET.get('page')
	if page is None:
		page = 1
	else:
		page = int(page)
	
	if request.GET.get('rec') == 'new':
		main_movies = Movie.objects().order_by('-date')
		slider_movies = main_movies[:5]
		category = 'Recommended Movies'	
		new_rec=True
		
	elif not authenticated_userid(request):
		main_movies = Movie.objects().order_by('-date')
		category = 'All Movies'
	else:
		main_movies = Movie.objects().order_by('date')
		slider_movies = main_movies[:5]
		category = 'Recommended Movies'
		right_movies['title']="More Recommendations"
	
	main_movies_title = 'Last updates'
	movies = dict(movies=main_movies[(page-1)*9:(page-1)*9+9], title=main_movies_title)
	slider_movies = slider_movies if slider_movies else Movie.objects()[rand:rand+5]
	return dict(movies=movies, slider_movies=slider_movies, right_movies=right_movies, category=category, page=page, new_rec=new_rec)

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
