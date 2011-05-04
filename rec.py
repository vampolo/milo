#!/usr/bin/python

#let's import the library we need
# if you don't have it you can download and install via pip (it's in python-pip ubuntu package)
#you can install suds with: sudo pip install suds
#i can import the suds library in my program now

from suds.client import Client

#let's do some logging

import logging

#this imports ipython shell so i can drop a shell when i want in the code
#having the context of the code being executed (easy debugger)
from IPython.Shell import IPShellEmbed
ipshell = IPShellEmbed()

#set up logging facility so we can see debug messages
logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)

#url of the wsdl
url = "http://intapps.moviri.com:8085/ws/RecoServerBean?wsdl"

#let's force the right location since the wsdl is WRONG!
location = "http://intapps.moviri.com:8085/ws/RecoServerBean"

#here the funny part starts... yeeeeeey :) it's for you Andreia :)
client = Client(url, location = location, username="demo", password="demo")

'''
This is a multiline python comment:
	client is the basic class we will use. it has mainly two methods: service and factory.
		service is used to call the webservices
		factory is used to create complex classes defined in the wsdl
'''

#now i create the data i need to do a test recommendation
caller = client.factory.create('CallerID')
caller.callerId = 'VOD_PORTAL'

#now i create the user class
user = client.factory.create('User')
user.userId = 2885178
user.usertype = 'TERMINAL'

#i set up the domain of the webservice, it's mandatory
subdomain = 'CW.VIDEO.NETFLIX'

#do the call and print result on the screen :P yeeeeeeeeey
print(client.service.getRec(caller, subdomain, user))

