from suds.client import Client
import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)

url = "http://intapps.moviri.com:8085/ws/RecoServerBean?wsdl"
location = "http://intapps.moviri.com:8085/ws/RecoServerBean"

class CWwrapper(object):
	def __init__(self):
		self.client = Client(url, location = location, username="demo", password="demo")
		self.caller = client.factory.create('CallerID')
		self.caller.callerId = 'VOD_PORTAL'
		slef.subdomain = 'CW.VIDEO.NETFLIX'
		
	def __get_cw_user(self, user):
		cwuser = self.client.factory.create('User')
		cwuser.userId = user.cwid
		cwuser.usertype = 'TERMINAL'
		return cwuser
		
	def get_rec(self, user):
		cwuser = self.__get_cw_user(user)
		res = client.service.getRec(self.caller, self.subdomain, cwuser)
		#what to do next ?


if __name__ == '__main__':
	import unittest
	
	class Test_CWwrapper(unittest.TestCase):
		def test_get_rec(self):
			pass
	
	unittest.main()
