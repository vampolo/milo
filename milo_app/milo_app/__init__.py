from pyramid.config import Configurator
from pyramid.events import subscriber
from pyramid.events import BeforeRender
from pyramid.renderers import get_renderer
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from milo_app.resources import Root
from milo_app import helpers
from milo_app.security import adminfinder

from mongoengine import connect

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    authn_policy = AuthTktAuthenticationPolicy(secret='miloSecretMessageForAuthToken', callback=adminfinder)
    authz_policy = ACLAuthorizationPolicy()
    my_session_factory = UnencryptedCookieSessionFactoryConfig('miloSecretMessageToSignTheCookie')
    config = Configurator(root_factory=Root, settings=settings,
    								authentication_policy=authn_policy,
    								authorization_policy=authz_policy,
    								session_factory = my_session_factory)
    config.add_subscriber(add_renderer_globals, BeforeRender)
    config.add_static_view('static', 'milo_app:static')
    config.add_static_view('css', 'milo_app:static/css')
    config.add_static_view('js', 'milo_app:static/js')
    config.add_static_view('images', 'milo_app:static/images')
    config.add_static_view('icons', 'milo_app:static/images/icons')
    config.scan()
    connect(settings['db_name'])
    return config.make_wsgi_app()

def add_renderer_globals(event):
	event.update({'base': get_renderer('templates/base.pt').implementation()})
	event.update({'admin_base': get_renderer('templates/admin.pt').implementation()})
	event.update({'h': helpers})
	
