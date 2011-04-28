from MediaRetriever import MediaRetriever
from resources import Movie
import urllib
import os

basepath = os.path.join(os.path.split(os.path.abspath( __file__ ))[0], 'static', 'movie_data')

class MovieManager(object):
	def add_movie_from_name(self, name=None):
		m = MediaRetriever(name)
		image = m.get_image()
		poster = m.get_poster()
		trailer = m.get_trailer()
		fi = open(os.path.join(basepath, name+'_image.jpg'), 'w')
		fi.write(urllib.urlopen(image).read())
		fp = open(os.path.join(basepath, name+'_poster.jpg'), 'w')
		fp.write(urllib.urlopen(poster).read())
		movie = Movie(title=name, image=name+'_image.jpg', poster=name+'_poster.jpg', trailer=trailer)
		print movie
		
		
if __name__ == '__main__':
	import unittest
	
	class Test_MovieManager(unittest.TestCase):
		def test_add_movie_from_name(self):
			mm = MovieManager()
			mm.add_movie_from_name(name='matrix')
	
	unittest.main()

