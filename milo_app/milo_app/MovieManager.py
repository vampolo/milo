from MediaRetriever import MediaRetriever
from resources import *
import urllib
import urllib2
import urlparse
import os
import datetime
import simplejson
from mongoengine import connect

basepath = os.path.join(os.path.split(os.path.abspath( __file__ ))[0], 'static', 'movie_data')

class MovieManager(object):
	def _whisperer_add_item(self, title):
		"""Create a whisperer item"""
		whisperer_url = 'http://whisperer.vincenzo-ampolo.net/item/add'
			#Using email to add the new user
		print 'title is', title, repr(title)
		data = urllib.urlencode(dict(name=title.encode('utf-8')))
		req = urllib2.Request(whisperer_url, data)
		while True:
				try:
					response = simplejson.load(urllib2.urlopen(req))
					break
				except urllib2.HTTPError:
					pass
				except:
					break
		return response
		
	def add_movie(self, name=None):
		m = MediaRetriever(name)
		image = m.get_image().get('image')
		d = m.get_info()
		poster = d.get('poster')
		description = d.get('description')
		year = d.get('year')
		#title = d.get('title')
		"""forget about imdb.com returned name... it's fake"""
		title = name.strip()
		genre = d.get('genre')
		try:
			trailer = m.get_trailer().get('trailer')
		except:
			trailer = None
		if not title:
			title = name
		title = unicode(title.replace('/','-'))
		filename=title
		if image is not None:
			fi = open(os.path.join(basepath, filename+'_image.jpg'), 'w')
			fi.write(urllib.urlopen(image).read())
		if poster is not None:
			fp = open(os.path.join(basepath, filename+'_poster.jpg'), 'w')
			fp.write(urllib.urlopen(poster).read())
		if not year:
			year = 1980
		if len(Movie.objects(title=title)) == 0:			
			#create a Whisperer Item
			i = 0
			while True:
				response = self._whisperer_add_item(title)
				if response.get('message') == 'Item already exists, please insert another':
					title = name + u'_'*i
					i = i + 1
				else:
					break
			
			if not description:
				description = u''
			else:
				description = unicode(description)		
			
			movie = Movie(title=title, whisperer_id=response['id'],date=datetime.datetime(year=int(year), month=1, day=1), description=description, image=filename+'_image.jpg', poster=filename+'_poster.jpg', trailer=trailer, genre=genre)
			print 'saving movie'
			print u'title: %s, whisperer_id: %s filename: %s, genre: %s' % (title, response['id'], filename, genre)
			movie.save()

			#Adding metadata
			#Shouldn't it add just if doesnt exist already this metadata? hmmm... here is doing both things at the same time?
			
			#YEAR
			#Create metadata and add to item -> loop to all metadata! -> example of the release date
			whisperer_url = 'http://whisperer.vincenzo-ampolo.net/item/'+str(movie.whisperer_id)+'/addMetadata'
			data = urllib.urlencode({'name':year,'type':'year','lang':'eng'})          
			req = urllib2.Request(whisperer_url, data)
			while True:
					try:
						response = simplejson.load(urllib2.urlopen(req))
						break
					except urllib2.HTTPError:
						pass
					except:
						break
			print response
			
			#GENRE
			for item in genre:
				whisperer_url = 'http://whisperer.vincenzo-ampolo.net/item/'+str(movie.whisperer_id)+'/addMetadata'
				data = urllib.urlencode({'name':item.encode("utf-8"),'type':'genre','lang':'eng'})          
				req = urllib2.Request(whisperer_url, data)
				while True:
					try:
						response = simplejson.load(urllib2.urlopen(req))
						break
					except urllib2.HTTPError:
						pass
					except:
						break
				print response	
			
			#ACTOR
			
			#DIRECTOR
			
			return movie
		return None
		
	def delete_movie(self, name=None):
		m = MediaRetriever(name)
		d = m.get_info()
		for movie in Movie.objects(title=d.get('title')):
			movie.save()
			for f_ile in [movie.poster, movie.image]:
				path = os.path.join(basepath, f_ile)
				if os.path.exists(path):
					os.remove(path)
			movie.delete()
			
	def import_movies_from_file(self, filename='/tmp/movie_titles.txt'):
		f = open(filename)
		#4917
		print f.readlines()[5000:5010]
		return
		for i,movie in enumerate(f.readlines()):
			print 'adding '+movie
			self.add_movie(name=movie)
	
def url_fix(s, charset='utf-8'):
    if isinstance(s, unicode):
        s = s.encode(charset, 'ignore')
    scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
    path = urllib.quote(path, '/%')
    qs = urllib.quote_plus(qs, ':&=')
    return urlparse.urlunsplit((scheme, netloc, path, qs, anchor))
			
if __name__ == '__main__':
	
	import unittest
	
	class Test_MovieManager(unittest.TestCase):
		def setUp(self):
			connect('milo')
			self.mm = MovieManager()
		
		def test_add_movie(self):
			for movie in ['the notebook', 'rio', 'matrix', 'caimano', 'matrix reload']:
				self.mm.add_movie(name=movie)
				m = MediaRetriever(movie)
				self.assertEqual(len(Movie.objects(title=m.get_info().get('title'))), 1)
		
		@unittest.skip("delete sucks")
		def test_delete_movie(self):
			for movie in ['the notebook', 'rio', 'matrix', 'caimano', 'matrix reload']:
				m = MediaRetriever(movie)
				self.mm.delete_movie(name=movie)
				self.assertEqual(len(Movie.objects(title=m.get_info().get('title'))), 0)
		
		
		def test_import_basic_movies(self):
			movies = ['rio', 'matrix', 'matrix reloaded',  'matrix revolutions', 'the notebook', 'along came polly',  'vanilla sky', 'batman begins', 'butterfly effect', 'the godfather', 'inception', 'city of god', 'forrest gump', 'finding nemo', 'back to the future', 'gladiator', "the king's speech", 'the milionaire', 'slumdog millionaire', 'kill bill', 'toy story 1', 'toy story 2', 'toy story 3', 'avatar', 'how to train your dragon', 'ratatouille', 'the social network', 'rocky', 'thron legacy', 'letters from iwo jima', 'il caimano', 'shutter island', 'monsters inc', 'v for vendetta', 'amores perros']
			for movie in movies:
				print 'adding '+movie
				self.mm.add_movie(name=movie)
				
#	unittest.main()
	
	#postgres to remove all the items and restart:
	#truncate table foo restart identity;
	#so it becomes:
	#truncate table public.item restart identity cascade;
	connect('milo')
	mm = MovieManager()
	mm.import_movies_from_file('/home/goshawk/whisperer/data/movie_titles.txt')
	
