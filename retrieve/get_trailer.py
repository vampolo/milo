import urllib
from lxml.html import parse

from ipdb import set_trace

movie_title = 'the matrix revolution'

page_search_list = parse(urllib.urlopen('http://www.youtube.com/results?'+urllib.urlencode({'search_query': movie_title+' trailer'})))

page_movie_trailer = page_search_list.xpath('//body/div/div/div/div/div/div/div/div/h3/a')[0].attrib.get('href')

trailer_id = page_movie_trailer[9:]

trailer_source = 'http://www.youtube.com/embed/'+trailer_id

print trailer_source