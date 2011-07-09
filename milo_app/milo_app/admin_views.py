from views import *
import datetime
import urllib, urllib2, simplejson, smtplib

@view_config(name='add_algorithm', context='milo_app:resources.Root',
				 renderer='templates/add_algorithm.pt', permission='admin')
@view_config(name='add_survey', context='milo_app:resources.Root',
				 renderer='templates/add_survey.pt', permission='admin')
@view_config(name='admin', context='milo_app:resources.Root',
				 renderer='templates/admin.pt', permission='admin')
def admin(request):
	name=''
	algorithm=''
	ratings=''
	typeRatings='2'
	set_users = ''
	status = True
	
	if 'submit.survey' in request.params:
		name = request.params['SurveyName']
		algorithm = request.params['survey_algorithm']
		ratings = request.params['NumSurveyRatings']
		typeRatings = request.params['TypeRatings']
		set_users = request.params['set_of_users'].split(';')
		#Check if all inputs are filled
		if name is not None and algorithm is not None and ratings is not None and set_users is not None:
			#Check if there is already this survey
			if Survey.objects.filter(name=name).first() is None:
				survey_added = Survey(name=name, algorithm=algorithm, typeRatings = int(typeRatings), number_of_ratings=int(ratings))
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
						user_added.save()
					else:
						user_added = User.objects.filter(email=item).first()
					#Send an email to user_added.email - sending individually
					SERVER = "localhost"
					FROM = "milosurvey@noreply.com"
					TO = user_added.email
					SUBJECT = "Milo's Survey Invitation"
					TEXT = "This is an invitation to participate on Milo survey." 
					TEXT1 ="Access http://milo.vincenzo-ampolo.net/wizard and enter this information to login:"
					TEXT2 = "Email: "+user_added.email	
					TEXT3 = 'Password: '+user_added.password
					# Prepare actual message
					message = """
					
					
					From: %s
					To: %s
					Subject: %s
					
					%s
					
					%s
					
					%s
					%s
					""" %( FROM,  TO, SUBJECT, TEXT, TEXT1, TEXT2, TEXT3 )
					# Send the mail
					server = smtplib.SMTP(SERVER)
					server.sendmail(FROM, TO, message)
					server.quit()
					
					survey_added.users.append(user_added)
					survey_added.last_updated_at = datetime.datetime.now()
					survey_added.status = status
					survey_added.save()
	
	#To vie wthe survey's table
	all_surveys = Survey.objects().order_by('name')
	surveys = dict(surveys=all_surveys[:])
	
	##To delete a survey from the DB
	#survey_name = request.GET.get('survey')
	#delete = request.GET.get('action')
	#if delete == 'delete':
		#Survey.objects.filter(name=survey_name).delete()
	
	#To change survey status (default when created is "ON")
	survey_name = request.GET.get('survey')
	change_status = request.GET.get('action')
	if change_status == 'turnon':
		survey_edited = Survey.objects.filter(name=survey_name).first()
		survey_edited.status = True
		status = True
		survey_edited.save()
	if change_status == 'turnoff':
		survey_edited = Survey.objects.filter(name=survey_name).first()
		survey_edited.status = False
		status = False
		survey_edited.save()
	
	algnames=[]
	num_algs=0
	#create a Whisperer User
	whisperer_url = 'http://whisperer.vincenzo-ampolo.net/algnames'
	req = urllib2.Request(whisperer_url)
	response = simplejson.load(urllib2.urlopen(req))					
	algnames = response['algnames']
	num_algs = len(algnames)
	
	
	return dict(surveys=surveys, algnames=algnames, num_algs=num_algs)

@view_config(name='view_users', context='milo_app:resources.Root',
				 renderer='templates/view_users.pt', permission='admin')
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
						user_added.save()
					else:
						user_added = User.objects.filter(email=item).first()
					#Send an email to user_added.email - sending individually
					SERVER = "localhost"
					FROM = "milosurvey@noreply.com"
					TO = user_added.email
					SUBJECT = "Milo's Survey Invitation"
					TEXT = "This is an invitation to participate on Milo survey." 
					TEXT1 ="Access http://milo.vincenzo-ampolo.net/wizard and enter this information to login:"
					TEXT2 = "Email: "+user_added.email	
					TEXT3 = 'Password: '+user_added.password
					# Prepare actual message
					message = """
					
					
					From: %s
					To: %s
					Subject: %s
					
					%s
					
					%s
					
					%s
					%s
					""" %( FROM,  TO, SUBJECT, TEXT, TEXT1, TEXT2, TEXT3 )
					# Send the mail
					server = smtplib.SMTP(SERVER)
					server.sendmail(FROM, TO, message)
					server.quit()
					current_survey.users.append(user_added)
					current_survey.last_updated_at = datetime.datetime.now()
					current_survey.save()
					return HTTPFound(location=request.resource_url(request.root, 'view_users', query=dict(survey=survey_name)))
	users = dict(users=users_objects_list[:])
	
	return dict(survey_name=survey_name, users=users)

@view_config(name='view_answers', context='milo_app:resources.Root',
				 renderer='templates/view_answers.pt', permission='admin')
def survey_answers(request):
	
	survey_name = request.GET.get('survey')
	current_survey = Survey.objects.filter(name=survey_name).first()
	answers_objects_list = current_survey.answers
	answers = dict(answers=answers_objects_list[:])
	
	return dict(survey_name=survey_name, answers=answers)
