import urllib2
import urllib
from lxml.html import parse

class MediaRetriever(object):
	def __init__(self, movie_title):
		self.movie_title = movie_title
		self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.24 (KHTML, like Gecko) Ubuntu/10.10 Chromium/12.0.703.0 Chrome/12.0.703.0 Safari/534.24'
	
	def __create_request(self, url, params=None):
		headers = { 'User-Agent' : self.user_agent }
		req = urllib2.Request(url, params, headers)
		return urllib2.urlopen(req)
		
	def get_image(self):
		movie_title = self.movie_title
		page_search_list = parse(urllib2.urlopen('http://moviepicturedb.com/browse/search?'+urllib.urlencode({'title': movie_title})))
		try:
			page_movie_gallery = page_search_list.xpath('//table/tr/td/strong/a')[0].attrib.get('href')
		except IndexError:
			return "not found"
		page_movie_gallery_wallpapers = parse(urllib2.urlopen(page_movie_gallery+'?cat_id=3'))
		try:
			page_movie_wallpaper = page_movie_gallery_wallpapers.xpath('//td/div/div/a')[0].attrib.get('href')
		except IndexError:
			#there are no pics in cat_id=3 for this movie
			page_movie_gallery_wallpapers = parse(urllib2.urlopen(page_movie_gallery))
			page_movie_wallpaper = page_movie_gallery_wallpapers.xpath('//td/div/div/a')[0].attrib.get('href')
		image_533x400 = parse(urllib2.urlopen(page_movie_wallpaper)).xpath('//body/div/div/div/div/img')[0].attrib.get('src')
		return dict(image=image_533x400)
		
	def get_poster(self):
		movie_title = self.movie_title
		page_search_list = parse(urllib2.urlopen('http://movieposterdb.com/browse/search?'+urllib.urlencode({'type':'movies', 'query': movie_title})))
		page_movie_gallery = page_search_list.xpath('//tr/td/b/a')[0].attrib.get('href')
		movie_poster_gallery = parse(urllib2.urlopen(page_movie_gallery))
		movie_poster = movie_poster_gallery.xpath('//tr/td/div/a/img')[0].attrib.get('src')
		return dict(poster=movie_poster)
		
	def get_trailer(self):
		movie_title = self.movie_title
		page_search_list = parse(urllib2.urlopen('http://www.youtube.com/results?'+urllib.urlencode({'search_query': movie_title+' trailer'})))
		page_movie_trailer = page_search_list.xpath('//body/div/div/div/div/div/div/div/div/h3/a')[0].attrib.get('href')
		trailer_id = page_movie_trailer[9:]
		trailer_source = 'http://www.youtube.com/embed/'+trailer_id
		return dict(trailer=trailer_source)
		
	def get_infos(self):
		movie = self.movie_title
		first_page = parse(self.__create_request('http://www.imdb.com/find?', urllib.urlencode({'s':'tt', 'q':movie})))
		second_page_url = first_page.xpath('//tr/td[3]/a')[0].attrib.get('href')
		second_page = parse(self.__create_request('http://www.imdb.com'+second_page_url))
		description = second_page.xpath("//div[@id='main']//table[@id='title-overview-widget-layout']//td[@id='overview-top']/p")[1].text
		year = second_page.xpath("//div[@id='main']//table[@id='title-overview-widget-layout']//td[@id='overview-top']/h1[@class='header']/span/a")[0].text
		poster_page_url = second_page.xpath("//div[@id='main']//table[@id='title-overview-widget-layout']//td[@id='img_primary']/a")[0].attrib.get('href')
		poster_page = parse(self.__create_request('http://www.imdb.com'+poster_page_url))
		poster_url = poster_page.xpath("//div[@id='photo-container']/div[@id='canvas']//img[@id='primary-img']")[0].attrib.get('src')
		return dict(year=year, description=description, poster=poster_url)

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
			
		def test_get_infos(self):
			for movie in ['rio', 'matrix', 'matrix reloaded', 'il caimano']:
				m = MediaRetriever(movie)
				for i in m.get_infos():
					self.assertNotEqual(i, None)
		
	unittest.main()
