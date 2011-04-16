import urllib
from lxml.html import parse

from ipdb import set_trace

movie_title = 'finding nemo'

page_search_list = parse(urllib.urlopen('http://moviepicturedb.com/browse/search?'+urllib.urlencode({'title': movie_title})))

page_movie_gallery = page_search_list.xpath('//table/tr/td/strong/a')[0].attrib.get('href')

page_movie_gallery_wallpapers = parse(urllib.urlopen(page_movie_gallery+'?cat_id=3'))

page_movie_wallpaper = page_movie_gallery_wallpapers.xpath('//td/div/div/a')[0].attrib.get('href')

image_533x400 = parse(urllib.urlopen(page_movie_wallpaper)).xpath('//body/div/div/div/div/img')[0].attrib.get('src')

print image_533x400
