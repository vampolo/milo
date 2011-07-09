from pyramid.httpexceptions import HTTPFound

from pyramid.security import remember
from pyramid.security import forget
from pyramid.view import view_config
from pyramid.url import resource_url
from pyramid.renderers import get_renderer
import urllib, urllib2, time, simplejson

from resources import User


@view_config(context='milo_app:resources.Root', name='login',
             renderer='templates/login_milo.pt')
@view_config(context='pyramid.exceptions.Forbidden',
             renderer='templates/login_milo.pt')
def login(request):
    basept = get_renderer('templates/base.pt').implementation()
    login_url = resource_url(request.context, request, 'login')
    referrer = request.url
    if referrer == login_url:
        referrer = request.application_url
    came_from = request.params.get('came_from', referrer)
    message = ''
    login = ''
    password = ''
    
    
    
    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        user = User.objects.filter(email=login).first()
        if user is not None and user.password == password:
			headers = remember(request, login)
			return HTTPFound(location = came_from,headers = headers)
		message = 'Failed login'
    
    if 'form.registration.submitted' in request.params:
		#we are in case of new user
		login = request.params['email']
		password = request.params['password']
		name = request.params['name']
		surname = request.params['surname']
		user = User.objects.filter(email=login).first()
		if user is None:
			#create a Whisperer User
			whisperer_url = 'http://whisperer.vincenzo-ampolo.net/user/add'
			#Using email to add the new user
			data = urllib.urlencode({'name':login})
			req = urllib2.Request(whisperer_url, data)
			response = simplejson.load(urllib2.urlopen(req))
			#Get the user id inside whisperer and store in Milo
			user = User(email=login, first_name=name, last_name=surname, password=password,whisperer_id=response['id'])
			user.save()
			headers = remember(request, login)
			return HTTPFound(location = came_from, headers = headers)
		message = 'User already exists' 
	
    return dict(
        message = message,
        url = request.application_url + '/login',
        came_from = came_from,
        login = login,
        password = password,
        base_pt = basept
        )
    
@view_config(context='milo_app:resources.Root', name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location = resource_url(request.context, request),
                     headers = headers)
    
@view_config(context='milo_app:resources.Root', name='exit')
def exit(request):
    return HTTPFound(location = resource_url(request.context, request, query=dict(wizard_movie='exit')))
    
