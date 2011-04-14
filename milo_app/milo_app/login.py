from pyramid.httpexceptions import HTTPFound

from pyramid.security import remember
from pyramid.security import forget
from pyramid.view import view_config
from pyramid.url import resource_url

from resources import User


@view_config(context='milo_app:resources.Root', name='login',
             renderer='templates/login.pt')
@view_config(context='pyramid.exceptions.Forbidden',
             renderer='templates/login.pt')
def login(request):
    login_url = resource_url(request.context, request, 'login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/' # never use the login form itself as came_from
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
            return HTTPFound(location = came_from,
                             headers = headers)
        message = 'Failed login'

    return dict(
        message = message,
        url = request.application_url + '/login',
        came_from = came_from,
        login = login,
        password = password,
        )
    
@view_config(context='milo_app:resources.Root', name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location = resource_url(request.context, request),
                     headers = headers)
    