from mongoengine import *

class Root(object):
    __name__= None
    __parent__= None
    
    def __init__(self, request):
		self.request = request
        
    def __getitem__(self, key):
		
		if key == "Movie":
			movie = Movie_wrap()
			movie.__parent__= self
			movie.__name__ = "Movie"
			return movie
		if key == "User":
			return User()
		raise KeyError

class User(Document):
	email = StringField(required=True)
	first_name = StringField()
	last_name = StringField()
	password = StringField()
	cwid = IntField()

class Comment(EmbeddedDocument):
	autor = ReferenceField(User)
	content = StringField()

class Genre(EmbeddedDocument):
	name = StringField()
	
class Movie_wrap(Document):
	__name__ = 'Movie_wrap'
	__parent__ = Root
	
	def __getitem__(self, key):
		if key == "wizard_movie":
			survey = Movie()
			survey.__parent__= self
			survey.__name__= "wizard_movie"
			return survey
		movie = Movie()
		movie.__parent__= self
		movie.__name__= "Movie"
		return movie


#class Survey(Document):
	#__name__ = 'Survey'
	#__parent__ = Movie_wrap
	
	#def __getitem__(self, key):			
		#self.movie_name = key
		#return KeyError
		
class Movie(Document):
	__name__ = 'Movie'
	__parent__ = Movie_wrap
	
	def __getitem__(self, key):			
		movie = Movie.objects(title = key).first()
		movie.__name__ = key
		movie.__parent__ = self
		return movie
		
	#movie is identified by title and year
	title = StringField(required=True)
	date = DateTimeField()
	description = StringField()
	trailer = URLField()
	poster = StringField()
	image = StringField()
	genre = ListField(StringField())
	comments = ListField(EmbeddedDocumentField(Comment))
	
	def __str__(self):
		return 'Movie(%s, %s, %s, %s, %s)' % (self.title, self.date, self.poster, self.image, self.trailer)

