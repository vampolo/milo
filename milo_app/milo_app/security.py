#For now is the only "admin" available!
#Login: admin 
#Password: miloadminpassword

def adminfinder(login, request):
	if login == 'admin':
		return ['admin']
	else:
		return []
