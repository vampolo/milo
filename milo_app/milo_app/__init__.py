from pyramid.config import Configurator
from milo_app.resources import Root

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory=Root, settings=settings)
    config.add_view('milo_app.views.my_view',
                    context='milo_app:resources.Root',
                    renderer='milo_app:templates/mytemplate.pt')
    config.add_static_view('static', 'milo_app:static')
    return config.make_wsgi_app()

