#For now is the only "admin" available!
#Login: admin 
#Password: miloadminpassword

USERS = {'admin':'admin'}
GROUPS = {'admin':['group:admin']}

def adminfinder(login, request):
    if login in USERS:
        return GROUPS.get(login, [])
