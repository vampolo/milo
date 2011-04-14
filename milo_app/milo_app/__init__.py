from pyramid.config import Configurator
from pyramid.events import subscriber
from pyramid.events import NewRequest
from milo_app.resources import Root

from mongoengine import connect


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory=Root, settings=settings)
    config.add_subscriber(add_mongoengine, NewRequest)
    config.add_view('milo_app.views.my_view',
                    context='milo_app:resources.Root',
                    renderer='milo_app:templates/mytemplate.pt')
    config.add_static_view('static', 'milo_app:static')
    config.scan()
    return config.make_wsgi_app()

def add_mongoengine(event):
	settings = event.request.registry.settings
	connect(settings['db_name'])
