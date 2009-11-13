from google.appengine.ext import db
# from django.contrib.auth.models import get_hexdigest, check_password

class ExamplePetitionModel(db.Model):
    # This is just like any other appengine model that you've ever written!
    name = db.StringProperty()
    email = db.EmailProperty()
    city = db.StringProperty()
    state = db.StringProperty()
    country = db.StringProperty()
    
class Agency(db.Model):
    name = db.StringProperty()
    tier = db.IntegerProperty()
    city = db.StringProperty()
    state = db.StringProperty()
    country = db.StringProperty()
    postal_code = db.IntegerProperty()
    agency_url = db.LinkProperty()
    executive = db.StringProperty()
    executive_email = db.EmailProperty()
    twitter = db.StringProperty()
    contact_email = db.EmailProperty()
    updated = db.DateTimeProperty()