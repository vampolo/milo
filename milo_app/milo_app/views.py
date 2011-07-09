from pyramid.view import view_config
from pyramid.renderers import get_renderer
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from resources import *
import urllib
import urllib2
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
@view_config(name='categories', context='milo_app:resources.Root',
				 renderer='templates/categories.pt')                     
def main(request):
	rand = random.randint(0, Movie.objects().count()-10)
	new_rec = None
	slider_movies = None
	right_movies = dict(movies=Movie.objects()[rand+5:rand+10], title="More Top Movies")
	wizard_movie = False
	filter_by = None
	session = request.session
	
	if request.GET.get('wizard_movie') == 'details':
		wizard_movie == True
        	
	#Next/Previous buttons to browse through the catalog
	page = request.GET.get('page')
	if page is None:
		page = 1
	else:
		page = int(page)
			
	#Set the "recommendations"
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
	
	#Title filter
	first_letter = request.GET.get('title')
	if first_letter is not None:
			filter_by = first_letter
			films_not_filtered = False
			main_movies = []
			for movie in Movie.objects().order_by('-date'):
				first_char = movie.title[0]
				if first_letter == first_char:
					main_movies.append(movie)
		
	#Genre filter
	genre = request.GET.get('genre')
	if genre is not None:
			filter_by = genre
			films_not_filtered = False
			main_movies = []
			for movie in Movie.objects().order_by('-date'):
				list_genre = movie.genre
				if genre in list_genre[:]:
					main_movies.append(movie)
	
	#Date filter
	date = request.GET.get('date')
	if date is not None:
			filter_by = date 
			films_not_filtered = False
			main_movies = []
			if int(date) is not 90: 
				if int(date) is not 80:
					for movie in Movie.objects().order_by('-date'):
						if movie.date.year == int(date):
							main_movies.append(movie)
			if int(date) is 90:
				years = [1999,1998,1997,1996,1995,1994,1993,1992,1991,1990]
				for movie in Movie.objects.all():
					if movie.date.year in years[:]:
						main_movies.append(movie)
			if int(date) is 80:
				years = [1989,1988,1987,1986,1985,1984,1983,1982,1981,1980]
				for movie in Movie.objects.all():
					if movie.date.year in years[:]:
						main_movies.append(movie)
	
	#Query Filter
	search_query = request.GET.get('search_query')
	#Search inside title, description, genre
	#In the future also for the actor, director, all metadata...
	if search_query is not None:
			filter_by = search_query
			capitalized_query = search_query.capitalize()
			films_not_filtered = False
			main_movies = []
			for movie in Movie.objects().order_by('-date'):
				list_title_strings = movie.title.split()
				list_description_strings = movie.description.split()
				list_strings_movie = []
				for item in list_title_strings:
					list_strings_movie.append(item)
				for item in list_description_strings:
					list_strings_movie.append(item)
				for item in movie.genre:
					list_strings_movie.append(item)
				if search_query in list_strings_movie:
					main_movies.append(movie)
				elif capitalized_query in list_strings_movie:
					main_movies.append(movie)
	main_movies_title = 'Last updates'
	#Compute and show pages
	last_page = True if len(main_movies) <= (page-1)*9+9 else False
	#Get 9 movies to be shown in the page
	movies = dict(movies=main_movies[(page-1)*9:(page-1)*9+9], title=main_movies_title)	
	#Movies in the slider are random for now
	slider_movies = slider_movies if slider_movies else Movie.objects()[rand:rand+5]
	
	#Check if is administrator
	#try:
		#login
		#if login == 'admin':
			#admin = True
	#except:
		#admin = False
	
	return dict(filter_by=filter_by,  wizard_movie = wizard_movie, movies=movies, slider_movies=slider_movies, right_movies=right_movies, category=category, page=page, last_page=last_page, new_rec=new_rec)

@view_config(name='about', context='milo_app:resources.Root',
				 renderer='templates/about.pt')
def about(request):
	return dict()

@view_config(name='profile', context='milo_app:resources.Root',
				 renderer='templates/profile.pt')
def profile(request):
	return dict()

@view_config(context='milo_app:resources.Movie',
				 renderer='templates/movie.pt')
def movie(context, request):
	
	if context.__parent__.__name__ == 'wizard_movie':
		request.override_renderer = 'templates/wizard_movie.pt'
	rand = random.randint(0, Movie.objects().count()-5)
	slider_movies = dict(movies=Movie.objects()[rand:rand+3], title='Related Movies')
	right_movies = dict(movies=Movie.objects()[rand+5:rand+10], title='Recommended by Friends')
	
	return dict(movie=context, slider_movies=slider_movies, right_movies=right_movies)
