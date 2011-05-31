from pyramid.view import view_config
from pyramid.renderers import get_renderer
from resources import *
from datetime import datetime
from pyramid.security import authenticated_userid
import random

@view_config(context='milo_app:resources.Root',
             renderer='templates/base.pt')
@view_config(name='Latest', context='milo_app:resources.Root',
             renderer='templates/movie_list.pt')
@view_config(name='Recommended', context='milo_app:resources.Root',
             renderer='templates/movie_list.pt')
@view_config(name='Popular', context='milo_app:resources.Root',
             renderer='templates/movie_list.pt')
@view_config(name='1', context='milo_app:resources.Root',
				 renderer='templates/step1.pt')
@view_config(name='2', context='milo_app:resources.Root',
				 renderer='templates/step2.pt')
@view_config(name='3', context='milo_app:resources.Root',
				 renderer='templates/step3.pt')
@view_config(name='4', context='milo_app:resources.Root',
				 renderer='templates/step4.pt')
@view_config(name='5', context='milo_app:resources.Root',
				 renderer='templates/step5.pt')
@view_config(name='finish', context='milo_app:resources.Root',
				 renderer='templates/finish.pt')                                                          
def main(request):
	rand = random.randint(0, Movie.objects().count()-10)
	new_rec = None
	rating_finished = None
	slider_movies = None
	right_movies = dict(movies=Movie.objects()[rand+5:rand+10], title="More Top Movies")
	wizard_movie = False
	
	if request.GET.get('wizard_movie') == 'details':
		wizard_movie == True
	
	#Testing Next/Previous buttons
	page = request.GET.get('page')
	if page is None:
		page = 1
	else:
		page = int(page)
	
	num_ratings = request.GET.get('num_ratings')
	
	if num_ratings is None:
		num_ratings = 1
	else:
		num_ratings = int(num_ratings)
		rating_finished=False
		
	if num_ratings == 6:
		rating_finished=True
	
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
	#compute and show pages
	last_page = True if len(main_movies) <= (page-1)*9+9 else False
	movies = dict(movies=main_movies[(page-1)*9:(page-1)*9+9], title=main_movies_title)
	rated_movies = Movie.objects()[:num_ratings]
	# the upper two lines are magic
	slider_movies = slider_movies if slider_movies else Movie.objects()[rand:rand+5]
	return dict(rated_movies = rated_movies, wizard_movie = wizard_movie, num_ratings = num_ratings, rating_finished=rating_finished, movies=movies, slider_movies=slider_movies, right_movies=right_movies, category=category, page=page, last_page=last_page, new_rec=new_rec)

@view_config(name='about', context='milo_app:resources.Root',
				 renderer='templates/about.pt')
def about(request):
	return dict()

@view_config(name='wizard', context='milo_app:resources.Root',
				 renderer='templates/wizard.pt')
def wizard(request):
	return dict()

#How do i append the view in the /wizard, instead of the root? to be /wizard/step1
#@view_config(name='1', context='milo_app:resources.Root',
#				 renderer='templates/step1.pt')
#@view_config(name='2', context='milo_app:resources.Root',
#				 renderer='templates/step2.pt')
#def step(request):
#	return dict()


@view_config(name='categories', context='milo_app:resources.Root',
				 renderer='templates/categories.pt')
def categories(request):
	return dict()

@view_config(name='profile', context='milo_app:resources.Root',
				 renderer='templates/profile.pt')
def profile(request):
	return dict()

@view_config(name='add_algorithm', context='milo_app:resources.Root',
				 renderer='templates/add_algorithm.pt')
@view_config(name='add_survey', context='milo_app:resources.Root',
				 renderer='templates/add_survey.pt')
@view_config(name='admin', context='milo_app:resources.Root',
				 renderer='templates/admin.pt')
def admin(request):
	return dict()

@view_config(name='wizard_movie',context='milo_app:resources.Movie',
				 renderer='templates/wizard_movie.pt')
@view_config(context='milo_app:resources.Movie',
				 renderer='templates/movie.pt')
def movie(context, request):
	rand = random.randint(0, Movie.objects().count()-5)
	slider_movies = dict(movies=Movie.objects()[rand:rand+3], title='Related Movies')
	right_movies = dict(movies=Movie.objects()[rand+5:rand+10], title='Recommended by Friends')
	
	return dict(movie=context, slider_movies=slider_movies, right_movies=right_movies)
