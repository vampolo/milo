from MediaRetriever import MediaRetriever
from resources import Movie
import urllib
import os
import datetime
from mongoengine import connect

basepath = os.path.join(os.path.split(os.path.abspath( __file__ ))[0], 'static', 'movie_data')

class MovieManager(object):
	def add_movie(self, name=None):
		m = MediaRetriever(name)
		image = m.get_image().get('image')
		d = m.get_infos()
		poster = d.get('poster')
		description = d.get('description')
		year = d.get('year')
		title = d.get('title')
		trailer = m.get_trailer().get('trailer')
		if image is not None:
			fi = open(os.path.join(basepath, name+'_image.jpg'), 'w')
			fi.write(urllib.urlopen(image).read())
		if poster is not None:
			fp = open(os.path.join(basepath, name+'_poster.jpg'), 'w')
			fp.write(urllib.urlopen(poster).read())
		if len(Movie.objects(title=title, date=datetime.datetime(year=int(year), month=1, day=1))) == 0:
			print 'adding ' + title
			movie = Movie(title=title, date=datetime.datetime(year=int(year), month=1, day=1), description=description, image=name+'_image.jpg', poster=name+'_poster.jpg', trailer=trailer)
			movie.save()
		else:
			print title+' already in database'
		
	def delete_movie(self, name=None):
		m = MediaRetriever(name)
		d = m.get_infos()
		for movie in Movie.objects(title=d.get('title')):
			os.remove(os.path.join(basepath, movie.poster))
			os.remove(os.path.join(basepath, movie.image))
			movie.delete()
			
		
if __name__ == '__main__':
	import unittest
	
	class Test_MovieManager(unittest.TestCase):
		def setUp(self):
			connect('milo')
			self.mm = MovieManager()
		
		def test_add_movie(self):
			for movie in ['rio', 'matrix', 'caimano', 'matrix reload']:
				self.mm.add_movie(name=movie)
				m = MediaRetriever(movie)
				self.assertEqual(len(Movie.objects(title=m.get_infos().get('title'))), 1)
		
		def test_delete_movie(self):
			print 'executing delete'
			for movie in ['rio', 'matrix', 'caimano', 'matrix reload']:
				self.mm.delete_movie(name=movie)
				self.assertEqual(len(Movie.objects(title=movie)), 0)
	
	unittest.main()

