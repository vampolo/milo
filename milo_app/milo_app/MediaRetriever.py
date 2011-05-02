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
		movie = self.movie_title
		first_page = parse(self.__create_request('http://www.imdb.com/find?', urllib.urlencode({'s':'tt', 'q':movie})))
		second_page_url = first_page.xpath('//tr/td[3]/a')[0].attrib.get('href')
		if second_page_url[0] != 'h':
			second_page = parse(self.__create_request('http://www.imdb.com'+second_page_url))
		else:
			#we are already in the ending page of the movie
			second_page = first_page
		try:
			image_page_url = second_page.xpath("//div[@id='main']//div[@class='mediastrip_container']//div[@class='mediastrip_container']//div[@class='see-more']/a")[0].attrib.get('href')
		except IndexError:
			image_page_url = None
			image_url = None
		if image_page_url is not None:
			image_page_list = parse(self.__create_request('http://www.imdb.com'+image_page_url))
			image_page = image_page_list.xpath("//div[@id='main']/div[@class='thumb_list']//a")[0].attrib.get('href') 
			image_url = image_page.xpath("//div[@id='main']/div[@class='thumb_list']//img")[0].attrib.get('src')
		return dict(image=image_url)
		
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
		page_movie_trailer = page_search_list.xpath("//div[@id='search-results']//h3/a")[0].attrib.get('href')
		trailer_id = page_movie_trailer[9:]
		trailer_source = 'http://www.youtube.com/embed/'+trailer_id
		return dict(trailer=trailer_source)
		
	def get_info(self):
		movie = self.movie_title
		genre = list()
		first_page = parse(self.__create_request('http://www.imdb.com/find?', urllib.urlencode({'s':'tt', 'q':movie})))
		second_page_url = first_page.xpath('//tr/td[3]/a')[0].attrib.get('href')
		if second_page_url[0] != 'h':
			second_page = parse(self.__create_request('http://www.imdb.com'+second_page_url))
		else:
			#we are already in the ending page of the movie
			second_page = first_page
			
		try:
			description = second_page.xpath("//div[@id='main']//table[@id='title-overview-widget-layout']//td[@id='overview-top']/p")[1].text.replace('\n', '')
		except IndexError:
			description = None
		try:		
			for i in second_page.xpath("//div[@id='main']//table[@id='title-overview-widget-layout']//td[@id='overview-top']//div[@class='infobar']/a"):
				genre.append(i.text)
		except IndexError:
			genre = None	
		try:
			year = second_page.xpath("//div[@id='main']//table[@id='title-overview-widget-layout']//td[@id='overview-top']/h1[@class='header']/span/a")[0].text
		except IndexError:
			year = None
		try:
			title = second_page.xpath("//div[@id='main']//table[@id='title-overview-widget-layout']//td[@id='overview-top']/h1[@class='header']")[0].text.replace('\n', '')
		except IndexError:
			title = None
		try:
			poster_page_url = second_page.xpath("//div[@id='main']//table[@id='title-overview-widget-layout']//td[@id='img_primary']/a")[0].attrib.get('href')
		except IndexError:
			poster_page_url = None
			poster_url = None
		if poster_page_url is not None:
			poster_page = parse(self.__create_request('http://www.imdb.com'+poster_page_url))
			poster_url = poster_page.xpath("//div[@id='photo-container']/div[@id='canvas']//img[@id='primary-img']")[0].attrib.get('src')
		return dict(title=title, genre=genre, year=year, description=description, poster=poster_url)

if __name__ == '__main__':
	import unittest
	
	class Test_MediaRetriever(unittest.TestCase):
		def test_image(self):
			m = MediaRetriever('the king speach')
			self.assertNotEqual(m.get_image(), None)
		
		def test_image_caimano(self):
			m = MediaRetriever('il caimano')
			#it does not exists in db
			self.assertNotEqual(m.get_image(), None)
		
		def test_get_infos(self):
			for movie in ['the king speach']:
				m = MediaRetriever(movie)
				for i in m.get_info():
					print m.get_info()
					self.assertNotEqual(i, None)
	
	unittest.main()
	
	
