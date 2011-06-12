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
	rating_finished = None
	slider_movies = None
	right_movies = dict(movies=Movie.objects()[rand+5:rand+10], title="More Top Movies")
	wizard_movie = False
	filter_by = None
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
	
	#Title filter
	first_letter = request.GET.get('title')
	if first_letter is not None:
			filter_by = first_letter
			films_not_filtered = False
			main_movies = []
			for movie in Movie.objects.all():
				first_char = movie.title[0]
				if first_letter == first_char:
					main_movies.append(movie)
		
	#Genre filter
	genre = request.GET.get('genre')
	if genre is not None:
			filter_by = genre
			films_not_filtered = False
			main_movies = []
			for movie in Movie.objects.all():
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
					for movie in Movie.objects.all():
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
	#in the future also for the actor...
	if search_query is not None:
			filter_by = search_query
			capitalized_query = search_query.capitalize()
			films_not_filtered = False
			main_movies = []
			for movie in Movie.objects.all():
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
	#compute and show pages
	last_page = True if len(main_movies) <= (page-1)*9+9 else False
	movies = dict(movies=main_movies[(page-1)*9:(page-1)*9+9], title=main_movies_title)
	rated_movies = Movie.objects()[:num_ratings]
	# the upper two lines are magic
	slider_movies = slider_movies if slider_movies else Movie.objects()[rand:rand+5]
	return dict(filter_by=filter_by, rated_movies = rated_movies, wizard_movie = wizard_movie, num_ratings = num_ratings, rating_finished=rating_finished, movies=movies, slider_movies=slider_movies, right_movies=right_movies, category=category, page=page, last_page=last_page, new_rec=new_rec)

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

##############################################################################################################

#separated in SURVEY_VIEWS and ADMIN_VIEWS

#@view_config(name='wizard', context='milo_app:resources.Root',
				 #renderer='templates/wizard.pt')
#@view_config(name='1', context='milo_app:resources.Survey',
				 #renderer='templates/step1.pt')
#@view_config(name='2', context='milo_app:resources.Survey',
				 #renderer='templates/step2.pt')
#@view_config(name='3', context='milo_app:resources.Survey',
				 #renderer='templates/step3.pt')
#@view_config(name='4', context='milo_app:resources.Survey',
				 #renderer='templates/step4.pt')
#@view_config(name='5', context='milo_app:resources.Survey',
				 #renderer='templates/step5.pt')
#@view_config(name='finish', context='milo_app:resources.Survey',
				 #renderer='templates/finish.pt')                                                          
#def survey(request):
	
	##Declare
	#rating_finished = None	
    
	##Session: control current step
	#session = request.session
	#user = None
	#email = ''
	#key = ''
	#message = ''
	#rated_movies = None
	
	##max_ratings = 0
	##survey_n_ratings = 0
	##Login in wizard and put user_login inside the session and the users list of the survey
	#if 'form.key.submitted' in request.params:
		#email = request.params['key_email']
		#key = request.params['key_password']
		#user = User.objects.filter(email=email).first()
		##For now the key is simply the password:
		#if user is not None:
			#if user.survey_status == 'submitted':
				#message = 'User has already submit this survey'
			#if user.survey_status is None:
				#if user.password == key:
##TESTAR SE ALGUEM TENTA "CORTAR SESSION"... DEVO ZERAR SESSION: ALERTA! DEPOIS O USER ANTES DEVE REFAZER
##TUDO...#DEVO APAGAR OQ FOI ADICIONADO NO SURVEY? SOH PEGAR ULTIMOS RESULTADOS...
					#try:
						#session['user']
						#print session['concluded_until_step']	
						#if session['user'] != user.email:
							#session['concluded_until_step'] = None
							#session['user'] = email
					#except:	
						#session['user'] = email
					##Use user in session to filter surveys and find the survey name, algorithm and ratings...
					#user_object_list = []
					#for item in Survey.objects.all():
						#user_object_list = item.users
						#for item_user in user_object_list:
							#if item_user.email == session['user']:
								#sur = Survey.objects.filter(name=item.name).first()
								#if sur is not None:
									#session['survey']=sur.name
									##Set the number of ratings
									#session['max_ratings'] = (int(sur.number_of_ratings))
									#session['ratings_executed'] = 0
									##Control until when the user finished the survey
									#try:
										#session['concluded_until_step']
									#except:
										#return HTTPFound(location = request.resource_url(request.root, 'Survey', '1'))
									#if session ['concluded_until_step'] is not None:
										#step_to_go = int(session['concluded_until_step'])+1
										#return HTTPFound(location = request.resource_url(request.root, 'Survey', str(step_to_go)))							
									#else:
										#return HTTPFound(location = request.resource_url(request.root, 'Survey', '1'))
		#if message == '':
			#message = 'User not registered in any survey or invalid password'
	
	
	##Control if session['max_ratings'] has been defined already (after login) or not
	#if request.view_name == 'wizard':
		#survey_n_ratings = 0
	#else:
		#survey_n_ratings = session['max_ratings']
		##Determine the size of the list showed (to be changed...)
		#rated_movies = Movie.objects()[:session['max_ratings']]
	
	##numero di ratings as a query now
	
	#if request.GET.get('rating') is not None:
		#session['ratings_executed'] = session['ratings_executed'] + 1
		#if session['ratings_executed'] == session['max_ratings']:		
			#rating_finished=True
			#session['concluded_until_step'] = request.view_name
		
		
	
	##Form submission Step 1
	
	#if 'form.info.submitted.1' in request.params:
			#session['concluded_until_step'] = request.view_name
			#user = User.objects.filter(email=session['user']).first()
			#age = SurveyAnswer(user = user, key='age', value=request.params['age'])
			#gender = SurveyAnswer(user = user, key='gender', value=request.params['sex'])
			#education = SurveyAnswer(user = user, key='education_lvl', value=request.params['edu'])
			#nationality = SurveyAnswer(user = user, key='nationality', value=request.params['country'])
			#avg_movies = SurveyAnswer(user = user, key='avg_movies', value=request.params['avg_movie'])
			#sur = Survey.objects.filter(name=session['survey']).first()
			#sur.answers.append(age)
			#sur.answers.append(gender)
			#sur.answers.append(education)
			#sur.answers.append(nationality)
			#sur.answers.append(avg_movies)
			#sur.save()
			#return HTTPFound(location=request.resource_url(request.root, 'Survey','2'))
	
	#movie_title = request.GET.get('movie_title')
	#rating = request.GET.get('rating')
	#if movie_title is not None:
		##Here we would accept just if the movie hasnt been rated
		##if SurveyAnswer.objects.filter(key=movie_title).first() == None:
##the right is to eliminate the rated movies from the list!
			#user = User.objects.filter(email=session['user']).first()
			#movie_rated = SurveyAnswer(user = user, key=movie_title, value=rating)
			#sur = Survey.objects.filter(name=session['survey']).first()
			#sur.answers.append(movie_rated)
			#sur.save()			

##Add RATING IN WHISPERER
			#whisperer_url = 'http://whisperer.vincenzo-ampolo.net/item/'+movie_title+'/addRating'
			#data = urllib.urlencode({'useremail':session['user'], 'rating':rating})          
			#req = urllib2.Request(whisperer_url, data)
			##Testing if it works -> should print in the command line the new user email and ID or an error message, if the user already exists (shouldn't be the case...)
			#response = urllib2.urlopen(req)
			#whisperer_page = response.read() 
			#print whisperer_page
			
	
	##Questions in step 3 and 4 might not be useful actually.... Should I take the answers?

	##Form submission step 3
	
	#specific = ''
	#missing = ''
	#missing1 = ''
	#missing2 = ''
	#complete = ''
	#if 'form.info.submitted.3' in request.params:
			#session['concluded_until_step'] = request.view_name
			#user = User.objects.filter(email=session['user']).first()
			#specific = SurveyAnswer(user = user, key='specific', value=request.params['specific'])
			#missing = SurveyAnswer(user = user, key='missing', value=request.params['missing'])
			#missing1 = SurveyAnswer(user = user, key='missing1', value=request.params['missing1'])
			#missing2 = SurveyAnswer(user = user, key='missing2', value=request.params['missing2'])
			#missing3 = SurveyAnswer(user = user, key='missing3', value=request.params['missing3'])
			#complete = SurveyAnswer(user = user, key='complete', value=request.params['complete'])
			#sur = Survey.objects.filter(name=session['survey']).first()
			#sur.answers.append(missing)
			#sur.answers.append(missing1)
			#sur.answers.append(missing2)
			#sur.answers.append(missing3)
			#sur.answers.append(complete)
			#sur.save()
			#return HTTPFound(location=request.resource_url(request.root, 'Survey','4'))
	
	##Form submission step 4 - I am not getting checklist information now because is actually "fake" questions... Should I?
	
	#confuse = ''
	#if 'form.info.submitted.4' in request.params:
			#session['concluded_until_step'] = request.view_name
			#user = User.objects.filter(email=session['user']).first()
			#confuse = SurveyAnswer(user = user, key='confuse', value=request.params['confuse'])
			#sur = Survey.objects.filter(name=session['survey']).first()
			#sur.answers.append(confuse)
			#sur.save()
			
##GENERATE THE RECOMMENDATION LIST
			#whisperer_url = 'http://whisperer.vincenzo-ampolo.net/user/'+session['user']+'/getRec'
			#data = urllib.urlencode({'alg':sur.algorithm})
			#req = urllib2.Request(whisperer_url, data)
##Testing if it works -> should print in the command line the new user email and ID or an error message, if the user already exists (shouldn't be the case...)
			#response = urllib2.urlopen(req)
			#whisperer_page = response.read() 
##OQ EU PEGO?!
			#print whisperer_page
			
			
			#return HTTPFound(location=request.resource_url(request.root, 'Survey','5'))
	
	##Form submission step 5 - loop for all movie list retrieved...
	
	#if 'form.info.submitted.5' in request.params:
			#session['concluded_until_step'] = request.view_name
			#user = User.objects.filter(email=session['user']).first()
			##confuse = SurveyAnswer(user = user, key='confuse', value=request.params['confuse'])
			##sur = Survey.objects.filter(name=session['survey']).first()
			##sur.answers.append(confuse)
			##sur.save()
			#return HTTPFound(location=request.resource_url(request.root, 'Survey','finish'))
	
	##Final form submission
	
	#if 'form.info.submitted.6' in request.params:
			#user = User.objects.filter(email=session['user']).first()
			#user.survey_status = 'submitted'
			#place = SurveyAnswer(user = user, key='place', value=request.params['place'])
			#reason = SurveyAnswer(user = user, key='reason', value=request.params['reason'])
			#sur = Survey.objects.filter(name=session['survey']).first()
			#sur.answers.append(place)
			#sur.answers.append(reason)
			#sur.save()
			#user.save()
			#print user.email
			#print user.survey_status
			##Where I will go when i click "continue"
			#session['concluded_until_step'] = None
			#session['user'] = None
			#return HTTPFound(location=request.resource_url(request.root, ''))
	
	##should be just inside the if...? or this flag is simply unuseful?
	#main_movies = Movie.objects().order_by('-date')
	#films_not_filtered = True
	
	#if films_not_filtered == True:
		##Get objects of DB to retrieve the movie catalogue
		#main_movies = Movie.objects().order_by('-date')
	
	##Filters in step 2
	##Title filter
	#first_letter = request.GET.get('title')
	#if first_letter is not None:
			#films_not_filtered = False
			#main_movies = []
			#for movie in Movie.objects.all():
				#first_char = movie.title[0]
				#if first_letter == first_char:
					#main_movies.append(movie)
		
	##Genre filter
	#genre = request.GET.get('genre')
	#if genre is not None:
			#films_not_filtered = False
			#main_movies = []
			#for movie in Movie.objects.all():
				#list_genre = movie.genre
				#if genre in list_genre[:]:
					#main_movies.append(movie)
	
	##Date filter
	#date = request.GET.get('date')
	#if date is not None:
			#films_not_filtered = False
			#main_movies = []
			#if int(date) is not 90: 
				#if int(date) is not 80:
					#for movie in Movie.objects.all():
						#if movie.date.year == int(date):
							#main_movies.append(movie)
			#if int(date) is 90:
				#years = [1999,1998,1997,1996,1995,1994,1993,1992,1991,1990]
				#for movie in Movie.objects.all():
					#if movie.date.year in years[:]:
						#main_movies.append(movie)
			#if int(date) is 80:
				#years = [1989,1988,1987,1986,1985,1984,1983,1982,1981,1980]
				#for movie in Movie.objects.all():
					#if movie.date.year in years[:]:
						#main_movies.append(movie)
	
	##Query Filter
	#search_query = request.GET.get('search_query')
	##Search inside title, description, genre
	##in the future also for the actor...
	#if search_query is not None:
			#capitalized_query = search_query.capitalize()
			#films_not_filtered = False
			#main_movies = []
			#for movie in Movie.objects.all():
				#list_title_strings = movie.title.split()
				#list_description_strings = movie.description.split()
				#list_strings_movie = []
				#for item in list_title_strings:
					#list_strings_movie.append(item)
				#for item in list_description_strings:
					#list_strings_movie.append(item)
				#for item in movie.genre:
					#list_strings_movie.append(item)
				#if search_query in list_strings_movie:
					#main_movies.append(movie)
				#elif capitalized_query in list_strings_movie:
					#main_movies.append(movie)
	
	##Testing Next/Previous buttons
	#page = request.GET.get('page')
	#if page is None:
		#page = 1
	#else:
		#page = int(page)
					
	##compute and show pages
	#last_page = True if len(main_movies) <= (page-1)*9+9 else False
	#movies = dict(movies=main_movies[(page-1)*9:(page-1)*9+9])
	
	#return dict(survey_n_ratings=survey_n_ratings,message = message, rated_movies = rated_movies, rating_finished = rating_finished, movies=movies, page=page, last_page=last_page)


#@view_config(name='add_algorithm', context='milo_app:resources.Root',
				 #renderer='templates/add_algorithm.pt')
#@view_config(name='add_survey', context='milo_app:resources.Root',
				 #renderer='templates/add_survey.pt')
#@view_config(name='admin', context='milo_app:resources.Root',
				 #renderer='templates/admin.pt')
#def admin(request):
	#name=''
	#algorithm=''
	#ratings=''
	#users = ''
	
	#print request.params
	#print request.view_name	
	#if 'submit.survey' in request.params:
		#print request.params
		#print request.view_name
		#name = request.params['SurveyName']
		#algorithm = request.params['survey_algorithm']
		#ratings = request.params['NumSurveyRatings']
		##Now users is just a bit string... I should separate them be the comma...
		#set_users = request.params['set_of_users'].split(';')
		##Check if all inputs are filled
		#if name is not None and algorithm is not None and ratings is not None and users is not None:
			##Check if there is already this survey
			#if Survey.objects.filter(name=name).first() is None:
				##users = ListField(ReferenceField(User))
				#survey_added = Survey(name=name, algorithm=algorithm, number_of_ratings=int(ratings))
				##Necessary?!
				#survey_added.save()
				##Append each item of users list above
				#for item in set_users:
					
##IF THE USER IS ALREADY IN DB, we will simply add to the list... if it is not, we will add a default key
##This is the current approach adopted in the case that the user will be registered only in one type of survey, never 2 surveys will be linked to a same email				
					#print User.objects.filter(email=item).first()
					
					#if User.objects.filter(email=item).first() is None:
						#user_added = User(email = item, password='defaultsurveykey')
						#user_added.save()
						
						##create a Whisperer User here
						#whisperer_url = 'http://whisperer.vincenzo-ampolo.net/user/add'
						#data = urllib.urlencode({'name':item})          
						#req = urllib2.Request(whisperer_url, data)
						##Testing if it works -> should print in the command line the new user email and ID or an error message, if the user already exists (shouldn't be the case...)
						#response = urllib2.urlopen(req)
						#whisperer_page = response.read() 
						#print whisperer_page
						
					#else:
						#user_added = User.objects.filter(email=item).first()
					
					#print user_added.email
					#print user_added.password	
					#survey_added.users.append(user_added)
					#survey_added.save()
	
	#all_surveys = Survey.objects().order_by('name')
	##surveys = dict(surveys=all_surveys[:], name= all_surveys_name)
	#surveys = dict(surveys=all_surveys[:])
	
	#survey_name = request.GET.get('survey')
	#delete = request.GET.get('action')
	#if delete == 'delete':
		#Survey.objects.filter(name=survey_name).delete()
		
	
	#return dict(surveys=surveys)

#@view_config(name='view_users', context='milo_app:resources.Root',
				 #renderer='templates/view_users.pt')
#def survey_users(request):
	
	#survey_name = request.GET.get('survey')
	
	#current_survey = Survey.objects.filter(name=survey_name).first()
	#users_objects_list = current_survey.users
	##email_list =[]
	##for item in users_objects_list:
	##	email_list.append(item.email)
	#users = dict(users=users_objects_list[:])
	#print users.get('users')
	
	#return dict(survey_name=survey_name, users=users)
