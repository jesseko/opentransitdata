from google.appengine.ext import db
# from django.contrib.auth.models import get_hexdigest, check_password

class PetitionModel(db.Model):
    # This is just like any other appengine model that you've ever written!
    name = db.StringProperty()
    email = db.EmailProperty()
    city = db.StringProperty()
    state = db.StringProperty()
    country = db.StringProperty()
