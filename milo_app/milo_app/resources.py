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
		if key == "Survey":
			survey = Survey()
			survey.__parent__ = self
			survey.__name__ = key
			return survey
		raise KeyError

class User(Document):
	email = StringField(required=True)
	first_name = StringField()
	last_name = StringField()
	password = StringField()
	whisperer_id = IntField()
	#The flag that defines if the user has submitted the survey: "None" or "submitted" (handling just one survey per email)
	survey_status = StringField()

#To login in the admin!
class Admin(Document):
	username = StringField(required=True)
	password = StringField()

#AND IF the user has already done the survey, but is added in another one???????????? Now it is just handling exclusively one survey...
#A user can receive different keys... should check the key, not the user.... can be a list of strings here!
	#surveys = ListField(EmbeddedDocumentField(SurveyRegistered))

class SurveyAnswer(EmbeddedDocument):
	user = ReferenceField(User)
	key = StringField()
	value = StringField()

class Survey(Document):
	__name__ = 'Survey'
	__parent__ = Root
	
	#data of a survey
	name = StringField(required=True)
	algorithm = StringField()
	number_of_ratings = IntField()
	answers = ListField(EmbeddedDocumentField(SurveyAnswer))
	users = ListField(ReferenceField(User))
	
	def __getitem__(self,key):
		if key == "Movie":
			movie = Movie_wrap()
			movie.__parent__= self
			movie.__name__ = "Movie"
			return movie
		raise KeyError
			

#This must be used to handle many surveys for each user... applied after....
class SurveyRegistered(EmbeddedDocument):
	survey = ReferenceField(Survey)
	survey_password = StringField()
	
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

