from pyramid.view import view_config
from resources import *
from MediaRetriever import MediaRetriever

@view_config(name='get_info', context='milo_app:resources.Movie',
             renderer='json')
def get_info(request):
	movie_name = request.GET.get('title')
	if not movie_name:
		return dict()
	m = MediaRetriever(movie_name)
	return dict(image=m.get_image(), poster=m.get_poster(), trailer=m.get_trailer())
