from pyramid.view import view_config
from resources import *
from MediaRetriever import MediaRetriever

@view_config(name='getTrailer', context='milo_app:resources.Movie',
             renderer='json')
@view_config(name='getPoster', context='milo_app:resources.Movie',
             renderer='json')
@view_config(name='getImage', context='milo_app:resources.Movie',
             renderer='json')
@view_config(name='getInfos', context='milo_app:resources.Movie',
             renderer='json')            
def get_info(request):
	movie_name = request.GET.get('title')
	if not movie_name:
		return dict()
	m = MediaRetriever(movie_name)
	d = dict(getImage = m.get_image, getPoster = m.get_poster, getTrailer= m.get_trailer, getInfos = m.get_infos)
	return d.get(request.view_name)()
