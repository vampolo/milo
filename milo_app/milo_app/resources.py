from mongoengine import *

class Root(object):
    def __init__(self, request):
        self.request = request

class User(Document):
	email = StringField(required=True)
	first_name = StringField()
	last_name = StringField()
	password = StringField()

class Comment(EmbeddedDocument):
	content = StringField()

class Movie(Document):
	title = StringField(required=True)
	date = DateTimeField(required=True)
	description = StringField()
	trailer = URLField()
	cover = URLField()
	comments = ListField(EmbeddedDocumentField(Comment))