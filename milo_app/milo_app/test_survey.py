from resources import *

connect('milo')


sur = Survey(name='test survey', algorithm='blabla', number_of_ratings=5)

#add users to the survey

user = User.objects.filter(email='test')

print user[0]
#add an user to the survey
sur.users.append(user[0])
print sur.users

#store a new answer from a user:
a = SurveyAnswer(user = user[0], key='my question', value='my response')

#adding answer to a survey
sur.answers.append(a)

sur.save()

"""
this is a check that everything is in database

goshawk@earth:~/Projects/milo/milo_app/milo_app$ mongo localhost
MongoDB shell version: 1.8.1
connecting to: localhost
> use milo
switched to db milo
> show collections
fs.chunks
movie
survey
system.indexes
user
> db.survey.find()
{ "_id" : ObjectId("4de7c09d85248817af000000"), "_types" : [ "Survey" ], "name" : "test survey", "algorithm" : "blabla", "number_of_ratings" : 5, "answers" : [
	{
		"_types" : [
			"SurveyAnswer"
		],
		"value" : "my response",
		"user" : {
			"$ref" : "user",
			"$id" : ObjectId("4da73d228524880bac000000")
		},
		"key" : "my question",
		"_cls" : "SurveyAnswer"
	}
], "_cls" : "Survey", "users" : [ { "$ref" : "user", "$id" : ObjectId("4da73d228524880bac000000") } ] }


GOTCHA :)

cinema tonight ? :)


"""
