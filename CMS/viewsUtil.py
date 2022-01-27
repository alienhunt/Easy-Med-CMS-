from django.shortcuts import redirect
from django.contrib.auth.models import auth


# to check if the session is not expired then modify the session
def modifySession(request):

    if 'user' not in request.session:

        auth.logout(request)
        print("logout")

        return False
    
    request.session.modified = True

    return request