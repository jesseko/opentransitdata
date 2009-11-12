# NOTE DAVEPECK
#
# I wrote this code to help you get sessions and users on django +appengine applications.
# It is NOT AT ALL INTERESTING if you don't need users. In fact, for opentransit, I've
# turned if off in the settings.py file. But I kept it here just in case...
#

def appengine_user(request):
    if request.user:
        return {'user': request.user, 'user_is_valid':request.user.is_valid}
    else:
        return {'user': None, 'user_is_valid':False}

