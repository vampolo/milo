from views import *
import urllib, urllib2, simplejson

@view_config(name='add_algorithm', context='milo_app:resources.Root',
				 renderer='templates/add_algorithm.pt')
@view_config(name='add_survey', context='milo_app:resources.Root',
				 renderer='templates/add_survey.pt')
@view_config(name='admin', context='milo_app:resources.Root',
				 renderer='templates/admin.pt')
def admin(request):
	name=''
	algorithm=''
	ratings=''
	set_users = ''
	
	if 'submit.survey' in request.params:
		name = request.params['SurveyName']
		algorithm = request.params['survey_algorithm']
		ratings = request.params['NumSurveyRatings']
		set_users = request.params['set_of_users'].split(';')
		#Check if all inputs are filled
		if name is not None and algorithm is not None and ratings is not None and set_users is not None:
			#Check if there is already this survey
			if Survey.objects.filter(name=name).first() is None:
				survey_added = Survey(name=name, algorithm=algorithm, number_of_ratings=int(ratings))
				survey_added.save()
				#Append each item of users list above
				for item in set_users:	
					#IF THE USER IS ALREADY IN DB, we will simply add to the list... if it is not, we will add a default key
					#This is the current approach adopted in the case that the user will be registered only in one type of survey, never 2 surveys will be linked to a same email
					if User.objects.filter(email=item).first() is None:
						#create a Whisperer User
						whisperer_url = 'http://whisperer.vincenzo-ampolo.net/user/add'
						#Using email to add the new user
						data = urllib.urlencode({'name':item})
						req = urllib2.Request(whisperer_url, data)
						response = simplejson.load(urllib2.urlopen(req))
						#Get the user id inside whisperer and store in Milo
						user_added = User(email = item, password='defaultsurveykey',whisperer_id=response['id'])
						print user_added.whisperer_id
						user_added.save()
					else:
						user_added = User.objects.filter(email=item).first()
					survey_added.users.append(user_added)
					survey_added.save()
	
	#To vie wthe survey's table
	all_surveys = Survey.objects().order_by('name')
	surveys = dict(surveys=all_surveys[:])
	
	#To delete a survey from the DB
	survey_name = request.GET.get('survey')
	delete = request.GET.get('action')
	if delete == 'delete':
		Survey.objects.filter(name=survey_name).delete()
	
	
	return dict(surveys=surveys)

@view_config(name='view_users', context='milo_app:resources.Root',
				 renderer='templates/view_users.pt')
def survey_users(request):
	
	#To be implemented in the future, is a Milo feature, to navigate around the web application 
	#and receive the recommendations
	
	survey_name = request.GET.get('survey')
	current_survey = Survey.objects.filter(name=survey_name).first()
	users_objects_list = current_survey.users
	#email_list =[]
	#for item in users_objects_list:
	#	email_list.append(item.email)
	set_users = ''
	if 'submit.survey.users' in request.params:
		set_users = request.params['set_of_users'].split(';')
		if set_users is not None:
				#Append each item of users list above
				for item in set_users:	
					#IF THE USER IS ALREADY IN DB, we will simply add to the list... if it is not, we will add a default key
					#This is the current approach adopted in the case that the user will be registered only in one type of survey, never 2 surveys will be linked to a same email
					if User.objects.filter(email=item).first() is None:
						#create a Whisperer User
						whisperer_url = 'http://whisperer.vincenzo-ampolo.net/user/add'
						#Using email to add the new user
						data = urllib.urlencode({'name':item})
						req = urllib2.Request(whisperer_url, data)
						response = simplejson.load(urllib2.urlopen(req))
						#Get the user id inside whisperer and storing in Milo
						user_added = User(email = item, password='defaultsurveykey',whisperer_id=response['id'])
						print user_added.whisperer_id
						user_added.save()
					else:
						user_added = User.objects.filter(email=item).first()
					current_survey.users.append(user_added)
					current_survey.save()
					return HTTPFound(location=request.resource_url(request.root, 'view_users', query=dict(survey=survey_name)))
	users = dict(users=users_objects_list[:])
	
	return dict(survey_name=survey_name, users=users)
