from mongoengine import *

connect('milo')

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
	year = DateTimeField(required=True)
	description = StringField()
	trailer = URLField()
	cover = FileField()
	comments = ListField(EmbeddedDocumentField(Comment))