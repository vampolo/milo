from pyramid.paster import get_app
application = get_app(
  'development.ini', 'main')