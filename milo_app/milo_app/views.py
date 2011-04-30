from pyramid.view import view_config
from pyramid.renderers import get_renderer
from resources import *
from datetime import datetime


@view_config(context='milo_app:resources.Root',
             renderer='templates/base.pt')
def main(request):
	return dict()

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
	movie = Movie.objects(title = context.title).first()
	return dict(movie=movie)
