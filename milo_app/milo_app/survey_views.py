from views import *
import time, datetime
import urllib
import datetime
import urllib2
import urlparse
import simplejson
import operator
from MovieManager import url_fix

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
@view_config(name='recMovie1', context='milo_app:resources.Step5',
				 renderer='templates/step5.pt')
@view_config(name='recMovie2', context='milo_app:resources.Step5',
				 renderer='templates/step5.pt')       
@view_config(name='recMovie3', context='milo_app:resources.Step5',
				 renderer='templates/step5.pt')
@view_config(name='recMovie4', context='milo_app:resources.Step5',
				 renderer='templates/step5.pt')                                                                 
@view_config(name='recMovie5', context='milo_app:resources.Step5',
				 renderer='templates/step5.pt')       
def survey(request):
	#Some declarations
	rating_finished = None	
	session = request.session
	user = None
	email = ''
	key = ''
	message = ''
	#Initialize rated movies
	try:
		session['rated_movies']
	except:
		session['rated_movies'] = []
	try:
		rated_movies
	except:
		rated_movies = []
	try:
		index_recMovie
	except:
		index_recMovie = 0
	try:
		recommended_movies
	except:
		recommended_movies = []			
	try:
		session['ratings']
	except:
		session['ratings'] = []
	try:
		main_movies
	except:
		main_movies = []
#NOW
	try:
		session['survey']
	except:
		session['survey'] = None
	
	try:
		session['rating_type']
	except:
		#Default is the like/dislike
		session['rating_type'] = 2
	#Login in wizard and put user_login inside the session and the users list of the survey
	if 'form.key.submitted' in request.params:
		#Then the user must rate again anyway...
		rated_movies = []
		session['rated_movies'] = []
		session['ratings'] = []
		session['rating_type'] = 2
		email = request.params['key_email']
		key = request.params['key_password']
		user = User.objects.filter(email=email).first()
		#For now the key is simply the password, if I wasn't registered before the password is "defaultsurveykey":
		if user is not None:
			if user.survey_status == 'submitted':
				message = 'User has already submit this survey'
			if user.survey_status is None:
				if user.password == key:
					try:
						session['user']
						if session['user'] != user.email:
							session['concluded_until_step'] = None
							session['user'] = email
					except:	
						session['user'] = email
					#Use user in session to filter surveys and find the survey name, algorithm and ratings...
					user_object_list = []
					for item in Survey.objects.all():
						user_object_list = item.users
						for item_user in user_object_list:
							if item_user.email == session['user']:
								sur = Survey.objects.filter(name=item.name).first()
								if sur is not None:
									#Check if new model has been created or not!
									#Call whisperer service that returns last model date
									whisperer_url = 'http://whisperer.vincenzo-ampolo.net/'+sur.algorithm+'/alg_date'
									req = urllib2.Request(whisperer_url)
									response = simplejson.load(urllib2.urlopen(req))
									if response['date'] is not 'null' and response['date'] is not None:
										#Convert response['date'] string to datetime
										model_last_date = datetime.datetime.fromtimestamp(time.mktime(time.strptime(response['date'], "%d/%m/%y %H:%M"))) 
										if model_last_date is not None:
											if model_last_date < sur.last_updated_at:
												message = 'Survey not yet activated. Please, try again later.'
									#Case in which the model has never been created
									if response['date'] == 'null':
										message = 'Survey not yet activated. Please, try again later.'
									if message == '':
										session['survey']=sur.name
										#Set the number of ratings to be executed
										session['max_ratings'] = (int(sur.number_of_ratings))
										session['ratings_executed'] = 0
										#Get if it is 5 stars or binary
										session['rating_type'] = sur.typeRatings
										#Control until when the user finished the survey
										try:
											session['concluded_until_step']
										except:
											#If the user goes to the first step of the survey, 
											#is better to clean all the registers of responses given by the user
											sur = Survey.objects.filter(name=session['survey']).first()
											for item in sur.answers:
												user = User.objects.filter(email=session['user']).first()
												if item.user == user:
													sur.answers.remove(item)
													sur.save()
											return HTTPFound(location = request.resource_url(request.root, 'Survey', '1'))
										if session ['concluded_until_step'] is not None:
											step_to_go = int(session['concluded_until_step'])+1
											if step_to_go == 5:
												return HTTPFound(location = request.resource_url(request.root, 'Survey', str(step_to_go), 'recMovie1'))
	#FIXME
											#elif step_to_go == 6:
											#	return HTTPFound(location = request.resource_url(request.root, 'Survey', 'finish')
											#else:
											return HTTPFound(location = request.resource_url(request.root, 'Survey', str(step_to_go)))
										#New user on the session
										else:
											#Again, it is better to clean all the registers of responses given by the user
											sur = Survey.objects.filter(name=session['survey']).first()
											for item in sur.answers:
												user = User.objects.filter(email=session['user']).first()
												if item.user == user:
	#CHECK IF IT IS REALLY REMOVING...
													sur.answers.remove(item)
													sur.save()
											return HTTPFound(location = request.resource_url(request.root, 'Survey', '1'))
		if message == '':
			message = 'User not registered in any survey or invalid password'
	
	
	ratings_stars = False
	#If the survey is of 5 stars type, receives 'ratings_stars' receives TRUE
	if session['rating_type'] == 5:
		ratings_stars = True
	
	#Control if session['max_ratings'] has been defined already (after login) or not
	if request.view_name == 'wizard':
		survey_n_ratings = 0
	else:
		survey_n_ratings = session['max_ratings']
		
	#Number di ratings as a query now
	if request.GET.get('rating') is not None:
		session['ratings_executed'] = session['ratings_executed'] + 1
		if session['ratings_executed'] == session['max_ratings']:		
			rating_finished=True
			session['concluded_until_step'] = request.view_name
		
	#Form submission Step 1
	if 'form.info.submitted.1' in request.params:			
			session['concluded_until_step'] = request.view_name
			user = User.objects.filter(email=session['user']).first()
			age = SurveyAnswer(user = user, key='age', value=request.params['age'])
			gender = SurveyAnswer(user = user, key='gender', value=request.params['sex'])
			education = SurveyAnswer(user = user, key='education_lvl', value=request.params['edu'])
			nationality = SurveyAnswer(user = user, key='nationality', value=request.params['country'])
			avg_movies = SurveyAnswer(user = user, key='avg_movies', value=request.params['avg_movie'])
			sur = Survey.objects.filter(name=session['survey']).first()
			sur.answers.append(age)
			sur.answers.append(gender)
			sur.answers.append(education)
			sur.answers.append(nationality)
			sur.answers.append(avg_movies)
			sur.save()
			return HTTPFound(location=request.resource_url(request.root, 'Survey','2'))
	
	#Rating submission in step 2
	
	movie_title = request.GET.get('movie_title')
	rating = request.GET.get('rating')
	if movie_title is not None:
			#Here we would accept just if the movie hasnt been rated
			user = User.objects.filter(email=session['user']).first()
			movie_rated = SurveyAnswer(user = user, key=movie_title, value=rating)
			sur = Survey.objects.filter(name=session['survey']).first()
			sur.answers.append(movie_rated)
			session['ratings'].append(rating)
			sur.save()			
			#APPEND THE RATED MOVIE TO THE RATED session LIST
			#Because of the limited size of the session, maybe it's better to retrieve the answers
			for item in Movie.objects.all():
					if item == Movie.objects.filter(title=movie_title).first():
						session['rated_movies'].append(item)			
	
	#Form submission step 3
	specific = ''
	missing = ''
	missing1 = ''
	missing2 = ''
	complete = ''
	if 'form.info.submitted.3' in request.params:
			session['concluded_until_step'] = request.view_name
			user = User.objects.filter(email=session['user']).first()
			specific = SurveyAnswer(user = user, key='specific', value=request.params['specific'])
			missing = SurveyAnswer(user = user, key='missing', value=request.params['missing'])
			missing1 = SurveyAnswer(user = user, key='missing1', value=request.params['missing1'])
			missing2 = SurveyAnswer(user = user, key='missing2', value=request.params['missing2'])
			missing3 = SurveyAnswer(user = user, key='missing3', value=request.params['missing3'])
			complete = SurveyAnswer(user = user, key='complete', value=request.params['complete'])
			sur = Survey.objects.filter(name=session['survey']).first()
			sur.answers.append(missing)
			sur.answers.append(missing1)
			sur.answers.append(missing2)
			sur.answers.append(missing3)
			sur.answers.append(complete)
			sur.save()
			return HTTPFound(location=request.resource_url(request.root, 'Survey','4'))
	
	#Form submission step 4 - I am not getting checklist information now because is actually "fake" questions
	confuse = ''
	if 'form.info.submitted.4' in request.params:
			session['concluded_until_step'] = request.view_name
			user = User.objects.filter(email=session['user']).first()
			confuse = SurveyAnswer(user = user, key='confuse', value=request.params['confuse'])
			sur = Survey.objects.filter(name=session['survey']).first()
			sur.answers.append(confuse)
			sur.save()			
			return HTTPFound(location=request.resource_url(request.root, 'Survey','5', 'recMovie1'))
	
	#Create the list of rated movies
	rated_movies = session['rated_movies']
	
	recMovie_views = ['recMovie1','recMovie2','recMovie3','recMovie4','recMovie5']
	#Get recommendation if the user is in step 5:
	if request.view_name in recMovie_views:
		user = User.objects.filter(email=session['user']).first()
		sur = Survey.objects.filter(name=session['survey']).first()
		if user.whisperer_id is not None:
						whisperer_url = 'http://whisperer.vincenzo-ampolo.net/user/'+str(user.whisperer_id)+'/getRec'
						data = urllib.urlencode({'alg':sur.algorithm})
						req = urllib2.Request(whisperer_url, data)
						response = simplejson.load(urllib2.urlopen(req))
						#order dictionary by the values, getting the bigger
						sorted_response = sorted(response.iteritems(), key=operator.itemgetter(1), reverse=True)
						#Sorted response is a list of tuples... I want a list of the first element of the tuple
						for movie_tuple in sorted_response:
							rec_movie_id = movie_tuple[0]
							#Create a list of movie objects just with the ones on Milo and not in rated_movies list
							#recommended_movies_ids.append(rec_movie_id)
							if Movie.objects.filter(whisperer_id=int(rec_movie_id)).first() is not None:
								movie = Movie.objects.filter(whisperer_id=int(rec_movie_id)).first()
								if movie not in rated_movies:
									recommended_movies.append(movie)
						#HERE WE CUT THE RECOMMENDED LIST IN THE NUMBER OF MOVIES WE WANT THE USER TO EVALUATE:
						recommended_movies = recommended_movies[0:5]
#MAYBE CAN BE SET BY THE ADMIN AGAIN...	
		
	#Then i must get the ids of the movies to retrieved to the user =]! Finally, step 5 can be implemented
	
	#Setting the right film index	
	if request.view_name == 'recMovie2':
		index_recMovie = 1
	if request.view_name == 'recMovie3':
		index_recMovie = 2
	if request.view_name == 'recMovie4':
		index_recMovie = 3
	if request.view_name == 'recMovie5':
		index_recMovie = 4
	
	#Form submission step 5 - loop for all movie list retrieved...
	seen = ''
	if 'form.info.submitted.5' in request.params:
			user = User.objects.filter(email=session['user']).first()
			seen = SurveyAnswer(user = user, key='seen '+recommended_movies[index_recMovie].title, value=request.params['seen'])
			sur = Survey.objects.filter(name=session['survey']).first()
			sur.answers.append(seen)
			#Adjustments necessary because of the javascript "hide"
			try:
				request.params['rating1']
				rating1 = SurveyAnswer(user = user, key='rating1 '+recommended_movies[index_recMovie].title, value=request.params['rating1'])
				sur.answers.append(rating1)
			except:
				rating1 = ''
			try:
				request.params['heard']
				heard = SurveyAnswer(user = user, key='heard '+recommended_movies[index_recMovie].title, value=request.params['heard'])
				sur.answers.append(heard)
			except:	
				heard = ''
			try:
				request.params['rating2']
				rating2 = SurveyAnswer(user = user, key='rating2 '+recommended_movies[index_recMovie].title, value=request.params['rating2'])
				sur.answers.append(rating2)
			except:
				rating2 = ''
			try:
				request.params['rating3']
				rating3 = SurveyAnswer(user = user, key='rating3 '+recommended_movies[index_recMovie].title, value=request.params['rating3'])
				sur.answers.append(rating3)
			except:
				rating3 = ''
			if sur is not None:
				sur.save()
			if request.view_name == 'recMovie1':
				return HTTPFound(location=request.resource_url(request.root, 'Survey','5','recMovie2'))
			if request.view_name == 'recMovie2':
				return HTTPFound(location=request.resource_url(request.root, 'Survey','5','recMovie3'))
			if request.view_name == 'recMovie3':
				return HTTPFound(location=request.resource_url(request.root, 'Survey','5','recMovie4'))
			if request.view_name == 'recMovie4':
				return HTTPFound(location=request.resource_url(request.root, 'Survey','5','recMovie5'))
			if request.view_name == 'recMovie5':
				session['concluded_until_step'] = 5
				return HTTPFound(location=request.resource_url(request.root, 'Survey','finish'))
	
	#Final form submission
	
	if 'form.info.submitted.6' in request.params:
			user = User.objects.filter(email=session['user']).first()
			user.survey_status = 'submitted'
			place = SurveyAnswer(user = user, key='place', value=request.params['place'])
			reason = SurveyAnswer(user = user, key='reason', value=request.params['reason'])
			sur = Survey.objects.filter(name=session['survey']).first()
			sur.answers.append(place)
			sur.answers.append(reason)
			sur.save()
			user.save()
			#Clean un session
			session['concluded_until_step'] = None
			session['user'] = None
			return HTTPFound(location=request.resource_url(request.root, ''))

########### Manage the movie list in step 2 ##########
	
	#Create complete movie list
	for movie in Movie.objects().order_by('-date'):
		if movie.whisperer_id is not None:
			main_movies.append(movie)
	
	#The ratings done until the moment
	ratings = session['ratings']
	
	#Deleting a movie from the final rated list
	deleted_movie = request.GET.get('delete')
	deleted_movie_index = request.GET.get('index')
	if deleted_movie is not None and deleted_movie_index is not None:
		del session['ratings'][int(deleted_movie_index)]
		for movie in Movie.objects().order_by('-date'):
				if movie.whisperer_id is not None:
					if deleted_movie == movie.title:
						session['rated_movies'].remove(movie)
						session['ratings_executed'] = session['ratings_executed'] - 1
						rating_finished=False
						session['concluded_until_step'] = 1
	
	
	
	#Create the list of rated movies without using session 
	#(remember to delete the answers that wont be used: just add the ones at the end... create a "submit.step2" to do it!)

	#Delete the rated movies from the main_list
	if rated_movies is not None:
			main_movies = []
			for movie in Movie.objects().order_by('-date'):
				if movie.whisperer_id is not None:
					if movie not in rated_movies:
						main_movies.append(movie)
	
	#Add RATINGS IN WHISPERER (Shouldnt be None, never actually)
	#JUST WHEN USER CONFIRMS THE FINAL LIST
	if 'form.info.submitted.2' in request.params:
			index = 0
			for movie in rated_movies:
				user = User.objects.filter(email=session['user']).first()
				if user.whisperer_id is not None:
					if movie.whisperer_id is not None:
						whisperer_url = 'http://whisperer.vincenzo-ampolo.net/item/'+str(movie.whisperer_id)+'/addRating'
						if session['ratings'][index] == 'like':
							data = urllib.urlencode({'userid':user.whisperer_id, 'rating':5})          
						if session['ratings'][index] == 'dislike':
							data = urllib.urlencode({'userid':user.whisperer_id, 'rating':1})
						if session['ratings'][index] == '1 star':
							data = urllib.urlencode({'userid':user.whisperer_id, 'rating':1})          
						if session['ratings'][index] == '2 stars':
							data = urllib.urlencode({'userid':user.whisperer_id, 'rating':2})
						if session['ratings'][index] == '3 stars':
							data = urllib.urlencode({'userid':user.whisperer_id, 'rating':3})          
						if session['ratings'][index] == '4 stars':
							data = urllib.urlencode({'userid':user.whisperer_id, 'rating':4})          
						if session['ratings'][index] == '5 stars':
							data = urllib.urlencode({'userid':user.whisperer_id, 'rating':5})
						req = urllib2.Request(whisperer_url, data)
						response = simplejson.load(urllib2.urlopen(req))
						index = index + 1
			return HTTPFound(location=request.resource_url(request.root, 'Survey','3'))
				
	#if session['survey'] is not None:
		#sur = Survey.objects.filter(name=session['survey']).first()
		#for item in sur.answers:
			#user = User.objects.filter(email=session['user']).first()
			#if item.user == user:
					#if item.value == 'like' or item.value == 'dislike':
						#print user.email
						#rated_movies.append(item.key)
						#print rated_movies
	
	#FILTERS
	#Title filter
	first_letter = request.GET.get('title')
	if first_letter is not None:
			main_movies = []
			for movie in Movie.objects().order_by('-date'):
				if movie.whisperer_id is not None:
					first_char = movie.title[0]
					if first_letter == first_char:
						if rated_movies is not None:
							if movie not in rated_movies:
								main_movies.append(movie)
						else:
							main_movies.append(movie)
	#Genre filter
	genre = request.GET.get('genre')
	if genre is not None:
			#films_not_filtered = False
			main_movies = []
			for movie in Movie.objects().order_by('-date'):
				if movie.whisperer_id is not None:
					list_genre = movie.genre
					if genre in list_genre[:]:
						if rated_movies is not None:
							if movie not in rated_movies:
								main_movies.append(movie)
						else:
							main_movies.append(movie)
	
	#Date filter
	date = request.GET.get('date')
	if date is not None:
			#films_not_filtered = False
			main_movies = []
			if int(date) is not 90: 
				if int(date) is not 80:
					for movie in Movie.objects().order_by('-date'):
						if movie.whisperer_id is not None:
							if movie.date.year == int(date):
								if rated_movies is not None:
									if movie not in rated_movies:
										main_movies.append(movie)
								else:
									main_movies.append(movie)
				if int(date) is 90:
					years = [1999,1998,1997,1996,1995,1994,1993,1992,1991,1990]
					for movie in Movie.objects.all():
						if movie.date.year in years[:]:
							if rated_movies is not None:
								if movie not in rated_movies:
									main_movies.append(movie)
							else:
								main_movies.append(movie)
				if int(date) is 80:
					years = [1989,1988,1987,1986,1985,1984,1983,1982,1981,1980]
					for movie in Movie.objects.all():
						if movie.date.year in years[:]:
							if rated_movies is not None:
								if movie not in rated_movies:
									main_movies.append(movie)
							else:
								main_movies.append(movie)
	
	#Query Filter
	search_query = request.GET.get('search_query')
	#Search inside title, description, genre
	#In the future also for the actor, director, all metadata...
	if search_query is not None:
			capitalized_query = search_query.capitalize()
			main_movies = []
			for movie in Movie.objects().order_by('-date'):
				if movie.whisperer_id is not None:
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
						if rated_movies is not None:
							if movie not in rated_movies:
								main_movies.append(movie)
						else:
							main_movies.append(movie)
					elif capitalized_query in list_strings_movie:
						if rated_movies is not None:
							if movie not in rated_movies:
								main_movies.append(movie)
						else:
							main_movies.append(movie)
	
	#Next/Previous buttons to browse the catalog
	page = request.GET.get('page')
	if page is None:
		page = 1
	else:
		page = int(page)
	
	#Control if it is the last page of movies
	last_page = True if len(main_movies) <= (page-1)*9+9 else False
	
	#Get the 9 movies to be shown
	movies = dict(movies=main_movies[(page-1)*9:(page-1)*9+9])
	
	return dict(ratings_stars = ratings_stars, index_recMovie = index_recMovie, recommended_movies = recommended_movies, ratings = ratings,survey_n_ratings=survey_n_ratings,message = message, rated_movies = rated_movies, rating_finished = rating_finished, movies=movies, page=page, last_page=last_page)
