from pyramid.paster import get_app
application = get_app(
  '/var/www/milo/milo_app/development.ini', 'main')
