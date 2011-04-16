import urllib
from lxml.html import parse

from ipdb import set_trace

movie_title = 'days of summer'

page_search_list = parse(urllib.urlopen('http://movieposterdb.com/browse/search?'+urllib.urlencode({'type':'movies', 'query': movie_title})))

page_movie_gallery = page_search_list.xpath('//tr/td/b/a')[0].attrib.get('href')

movie_poster_gallery = parse(urllib.urlopen(page_movie_gallery))

movie_poster = movie_poster_gallery.xpath('//tr/td/div/a/img')[0].attrib.get('src')

print movie_poster


