from pyramid.view import view_config
from pyramid.renderers import get_renderer
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
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
def main(request):
	rand = random.randint(0, Movie.objects().count()-10)
	new_rec = None
	rating_finished = None
	slider_movies = None
	right_movies = dict(movies=Movie.objects()[rand+5:rand+10], title="More Top Movies")
	wizard_movie = False
	session = request.session
	
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

@view_config(context='milo_app:resources.Movie',
				 renderer='templates/movie.pt')
def movie(context, request):
	
	if context.__parent__.__name__ == 'wizard_movie':
		request.override_renderer = 'templates/wizard_movie.pt'
	rand = random.randint(0, Movie.objects().count()-5)
	slider_movies = dict(movies=Movie.objects()[rand:rand+3], title='Related Movies')
	right_movies = dict(movies=Movie.objects()[rand+5:rand+10], title='Recommended by Friends')
	
	return dict(movie=context, slider_movies=slider_movies, right_movies=right_movies)

@view_config(name='wizard', context='milo_app:resources.Root',
				 renderer='templates/wizard.pt')
@view_config(name='1', context='milo_app:resources.Survey',
				 renderer='templates/step1.pt')
@view_config(name='2', context='milo_app:resources.Survey',
				 renderer='templates/step2.pt')
@view_config(name='3', context='milo_app:resources.Survey',
				 renderer='templates/step3.pt')
@view_config(name='4', context='milo_app:resources.Survey',
				 renderer='templates/step4.pt')
@view_config(name='5', context='milo_app:resources.Survey',
				 renderer='templates/step5.pt')
@view_config(name='finish', context='milo_app:resources.Survey',
				 renderer='templates/finish.pt')                                                          
def survey(request):
	
	#Survey instance... Should be set in the admin
	sur = Survey(name='test survey', algorithm='algorithm#1', number_of_ratings=5)
	
	#Declare
	rating_finished = None
    
	#Session: control current step
	session = request.session
	session['step'] = request.view_name
	
	
	email = ''
	#Login in wizard and put user_login inside the session and the users list of the survey
	if 'form.key.submitted' in request.params:
		email = request.params['key_email']
		key = request.params['key_password']
		user = User.objects.filter(email=email).first()
		if user is not None and user.password == key:
			sur.users.append(user)
			sur.save()
			session['user'] = email
			return HTTPFound(location = request.resource_url(request.root, 'Survey','1'))
	
	#Testing Next/Previous buttons
	page = request.GET.get('page')
	if page is None:
		page = 1
	else:
		page = int(page)
	
	#Set the number of ratings
	max_ratings = (int(sur.number_of_ratings) + 1)
	#numero di ratings as a query now
	num_ratings = request.GET.get('num_ratings')
	if num_ratings is None:
		num_ratings = 1
	else:
		num_ratings = int(num_ratings)
		rating_finished=False
	
	if num_ratings == max_ratings:
		rating_finished=True
		
	#Get objects of DB to retrieve the movie catalogue
	main_movies = Movie.objects().order_by('-date')
	
	#compute and show pages
	last_page = True if len(main_movies) <= (page-1)*9+9 else False
	movies = dict(movies=main_movies[(page-1)*9:(page-1)*9+9])
	#Show the list of rated movies in step 2
	rated_movies = Movie.objects()[:num_ratings]
	
	#Initialize the Step 1 inputs
	#Form submission step 1
	if 'form.info.submitted.1' in request.params:
			user = User.objects.filter(email=session['user']).first()
			age = SurveyAnswer(user = user, key='age', value=request.params['age'])
			gender = SurveyAnswer(user = user, key='gender', value=request.params['sex'])
			nationality = SurveyAnswer(user = user, key='nationality', value=request.params['country'])
			avg_movies = SurveyAnswer(user = user, key='avg_movies', value=request.params['avg_movie'])
			sur.answers.append(age)
			sur.answers.append(gender)
			sur.answers.append(nationality)
			sur.answers.append(avg_movies)
			sur.save()
			return HTTPFound(location=request.resource_url(request.root, 'Survey','2'))
	
	#Form submission step 2 - deal with number of ratings... like now or put in the session?
	if 'form.info.submitted.2' in request.params:
			user = User.objects.filter(email=session['user']).first()
			#confuse = SurveyAnswer(user = user, key='confuse', value=request.params['confuse'])
			#sur.answers.append(confuse)
			#sur.save()
			return HTTPFound(location=request.resource_url(request.root, 'Survey','3'))
	
	#Questions in step 3 and 4 might not be useful actually.... Should I take the answers?

	#Form submission step 3
	if 'form.info.submitted.3' in request.params:
			user = User.objects.filter(email=session['user']).first()
			specific = SurveyAnswer(user = user, key='specific', value=request.params['specific'])
			missing = SurveyAnswer(user = user, key='missing', value=request.params['missing'])
			missing1 = SurveyAnswer(user = user, key='missing1', value=request.params['missing1'])
			missing2 = SurveyAnswer(user = user, key='missing2', value=request.params['missing2'])
			missing3 = SurveyAnswer(user = user, key='missing3', value=request.params['missing3'])
			complete = SurveyAnswer(user = user, key='complete', value=request.params['complete'])
			sur.answers.append(missing)
			sur.answers.append(missing1)
			sur.answers.append(missing2)
			sur.answers.append(missing3)
			sur.answers.append(complete)
			sur.save()
			return HTTPFound(location=request.resource_url(request.root, 'Survey','4'))
	
	#Form submission step 4 - I am not getting checklist information now because is actually "fake" questions... Should I?
	if 'form.info.submitted.4' in request.params:
			user = User.objects.filter(email=session['user']).first()
			confuse = SurveyAnswer(user = user, key='confuse', value=request.params['confuse'])
			sur.answers.append(confuse)
			sur.save()
			return HTTPFound(location=request.resource_url(request.root, 'Survey','5'))
	
	#Form submission step 5 - loop for all movie list retrieved...
	if 'form.info.submitted.5' in request.params:
			user = User.objects.filter(email=session['user']).first()
			#confuse = SurveyAnswer(user = user, key='confuse', value=request.params['confuse'])
			#sur.answers.append(confuse)
			#sur.save()
			return HTTPFound(location=request.resource_url(request.root, 'Survey','finish'))
	
	#Final form submission
	if 'form.info.submitted.6' in request.params:
			user = User.objects.filter(email=session['user']).first()
			place = SurveyAnswer(user = user, key='place', value=request.params['place'])
			reason = SurveyAnswer(user = user, key='reason', value=request.params['reason'])
			sur.answers.append(place)
			sur.answers.append(reason)
			sur.save()
			#Where I will go when i click "continue"
			return HTTPFound(location=request.resource_url(request.root, ''))
	
	return dict(rated_movies = rated_movies, num_ratings = num_ratings,rating_finished = rating_finished, movies=movies, page=page, last_page=last_page)
