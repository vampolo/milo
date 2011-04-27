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
	basept = get_renderer('templates/base.pt').implementation()
	return dict(base_pt=basept)

@view_config(name='categories', context='milo_app:resources.Root',
				 renderer='templates/categories.pt')
def categories(request):
	basept = get_renderer('templates/base.pt').implementation()
	return dict(base_pt=basept)
