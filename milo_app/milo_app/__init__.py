from pyramid.config import Configurator
from pyramid.events import subscriber
from pyramid.events import BeforeRender
from milo_app.resources import Root
from milo_app import helpers

from mongoengine import connect

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    authn_policy = AuthTktAuthenticationPolicy(secret='miloSecretMessageForAuthToken')
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(root_factory=Root, settings=settings,
    								authentication_policy=authn_policy,
    								authorization_policy=authz_policy)
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
	event['h'] = helpers 
