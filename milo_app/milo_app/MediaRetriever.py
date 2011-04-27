import urllib
from lxml.html import parse

class MediaRetriever(object):
	def __init__(self, movie_title):
		self.movie_title = movie_title
		
	def get_image(self):
		movie_title = self.movie_title
		page_search_list = parse(urllib.urlopen('http://moviepicturedb.com/browse/search?'+urllib.urlencode({'title': movie_title})))
		try:
			page_movie_gallery = page_search_list.xpath('//table/tr/td/strong/a')[0].attrib.get('href')
		except IndexError:
			return "not found"
		page_movie_gallery_wallpapers = parse(urllib.urlopen(page_movie_gallery+'?cat_id=3'))
		try:
			page_movie_wallpaper = page_movie_gallery_wallpapers.xpath('//td/div/div/a')[0].attrib.get('href')
		except IndexError:
			#there are no pics in cat_id=3 for this movie
			page_movie_gallery_wallpapers = parse(urllib.urlopen(page_movie_gallery))
			page_movie_wallpaper = page_movie_gallery_wallpapers.xpath('//td/div/div/a')[0].attrib.get('href')
		image_533x400 = parse(urllib.urlopen(page_movie_wallpaper)).xpath('//body/div/div/div/div/img')[0].attrib.get('src')
		return image_533x400
		
	def get_poster(self):
		movie_title = self.movie_title
		page_search_list = parse(urllib.urlopen('http://movieposterdb.com/browse/search?'+urllib.urlencode({'type':'movies', 'query': movie_title})))
		page_movie_gallery = page_search_list.xpath('//tr/td/b/a')[0].attrib.get('href')
		movie_poster_gallery = parse(urllib.urlopen(page_movie_gallery))
		movie_poster = movie_poster_gallery.xpath('//tr/td/div/a/img')[0].attrib.get('src')
		return movie_poster
		
	def get_trailer(self):
		movie_title = self.movie_title
		page_search_list = parse(urllib.urlopen('http://www.youtube.com/results?'+urllib.urlencode({'search_query': movie_title+' trailer'})))
		page_movie_trailer = page_search_list.xpath('//body/div/div/div/div/div/div/div/div/h3/a')[0].attrib.get('href')
		trailer_id = page_movie_trailer[9:]
		trailer_source = 'http://www.youtube.com/embed/'+trailer_id
		return trailer_source

if __name__ == '__main__':
	import unittest
	
	class Test_MediaRetriever(unittest.TestCase):
		def test_image(self):
			m = MediaRetriever('matrix')
			self.assertNotEqual(m.get_image(), None)
			
		def test_image_caimano(self):
			m = MediaRetriever('il caimano')
			#it does not exists in db
			self.assertNotEqual(m.get_image(), None)
	
	unittest.main()
