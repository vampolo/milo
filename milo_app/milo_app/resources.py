from mongoengine import *
from suds.client import Client
from pyramid.threadlocal import get_current_registry

class Root(object):
    __name__= None
    __parent__= None
    def __init__(self, request):
        self.request = request
    def __getitem__(self, key):
		if key == "Movie":
			return Movie()
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

class Movie(Document):
	#movie is identified by tile and year
	title = StringField(required=True)
	date = DateTimeField(required=True)
	description = StringField()
	trailer = URLField()
	cover = URLField()
	comments = ListField(EmbeddedDocumentField(Comment))
