from pyramid.view import view_config
from pyramid.renderers import get_renderer
from resources import *
from datetime import datetime


@view_config(context='milo_app:resources.Root',
             renderer='templates/base.pt')
def main(request):
	if request.GET.get('rec') == 'new':
		movies = Movie.objects()[9:18]
	else:
		movies = Movie.objects().order_by('-date')
	slider_movies = Movie.objects()[18:]
	right_movies = dict(movies=Movie.objects()[5:8], title="Top Movies")
	return dict(movies=movies, slider_movies=slider_movies, right_movies=right_movies)

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
