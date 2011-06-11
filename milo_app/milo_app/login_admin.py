#from pyramid.httpexceptions import HTTPFound
#from pyramid.security import remember
#from pyramid.security import forget
#from pyramid.view import view_config
#from pyramid.url import resource_url
#from pyramid.renderers import get_renderer
#import urllib, urllib2, time

#from resources import Admin


#@view_config(context='milo_app:resources.Root', name='login_admin',
             #renderer='templates/login_admin.pt')
#@view_config(context='pyramid.exceptions.Forbidden',
             #renderer='templates/login_admin.pt')
#def login_admin(request):
    #basept = get_renderer('templates/admin.pt').implementation()
    #login_url = resource_url(request.context, request, 'login_admin')
    #referrer = request.url
    #if referrer == login_url:
        #referrer = request.application_url
    #message = ''
    #login = ''
    #password = ''
    #if 'form.submitted' in request.params:
        #login = request.params['login']
        #password = request.params['password']
        #admin = Admin.objects.filter(username=login).first()
        #if admin is not None and admin.password == password:
            #headers = remember(request, login)
            #return HTTPFound(headers = headers)
        #message = 'Failed login'
	
    #return dict(
        #message = message,
        #url = request.application_url + '/login_admin',
        #login = login,
        #password = password,
        #base_pt = basept
        #)
    
#@view_config(context='milo_app:resources.Root', name='logout')
#def logout(request):
#    headers = forget(request)
#    return HTTPFound(location = resource_url(request.context, request),
#                     headers = headers)
    
#@view_config(context='milo_app:resources.Root', name='exit')
#def exit(request):
#    return HTTPFound(location = resource_url(request.context, request, query=dict(wizard_movie='exit')))
    
