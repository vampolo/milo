from views import *
import urllib
import urllib2

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
	users = ''
	
	if 'submit.survey' in request.params:
		name = request.params['SurveyName']
		algorithm = request.params['survey_algorithm']
		ratings = request.params['NumSurveyRatings']
		#Now users is just a bit string... I should separate them be the comma...
		set_users = request.params['set_of_users'].split(';')
		#Check if all inputs are filled
		if name is not None and algorithm is not None and ratings is not None and users is not None:
			#Check if there is already this survey
			if Survey.objects.filter(name=name).first() is None:
				#users = ListField(ReferenceField(User))
				survey_added = Survey(name=name, algorithm=algorithm, number_of_ratings=int(ratings))
				#Necessary?!
				survey_added.save()
				#Append each item of users list above
				for item in set_users:
					
#IF THE USER IS ALREADY IN DB, we will simply add to the list... if it is not, we will add a default key
#This is the current approach adopted in the case that the user will be registered only in one type of survey, never 2 surveys will be linked to a same email				
					
					if User.objects.filter(email=item).first() is None:
						user_added = User(email = item, password='defaultsurveykey')
						user_added.save()
						#create a Whisperer User here
						whisperer_url = 'http://whisperer.vincenzo-ampolo.net/user/add'
						data = urllib.urlencode({'name':item})
						req = urllib2.Request(whisperer_url, data)
						#Testing if it works -> should print in the command line the new user email and ID or an error message, if the user already exists (shouldn't be the case...)
						response = urllib2.urlopen(req)
						whisperer_page = response.read() 
						print whisperer_page
					else:
						user_added = User.objects.filter(email=item).first()
					survey_added.users.append(user_added)
					survey_added.save()
	
	all_surveys = Survey.objects().order_by('name')
	#surveys = dict(surveys=all_surveys[:], name= all_surveys_name)
	surveys = dict(surveys=all_surveys[:])
	
	survey_name = request.GET.get('survey')
	delete = request.GET.get('action')
	if delete == 'delete':
		Survey.objects.filter(name=survey_name).delete()
		
	
	return dict(surveys=surveys)

@view_config(name='view_users', context='milo_app:resources.Root',
				 renderer='templates/view_users.pt')
def survey_users(request):
	
	survey_name = request.GET.get('survey')
	
	current_survey = Survey.objects.filter(name=survey_name).first()
	users_objects_list = current_survey.users
	#email_list =[]
	#for item in users_objects_list:
	#	email_list.append(item.email)
	users = dict(users=users_objects_list[:])
	
	return dict(survey_name=survey_name, users=users)
