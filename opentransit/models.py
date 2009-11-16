from google.appengine.ext import db
# from django.contrib.auth.models import get_hexdigest, check_password

class PetitionModel(db.Model):
    # This is just like any other appengine model that you've ever written!
    name = db.StringProperty()
    email = db.EmailProperty()
    city = db.StringProperty()
    state = db.StringProperty()
    country = db.StringProperty()
    
class Agency(db.Model):
    name            = db.StringProperty()
    short_name      = db.StringProperty()
    tier            = db.IntegerProperty()
    city            = db.StringProperty()
    state           = db.StringProperty()
    country         = db.StringProperty()
    postal_code     = db.IntegerProperty()
    address         = db.StringProperty()
    agency_url      = db.LinkProperty()
    executive       = db.StringProperty()
    executive_email = db.EmailProperty()
    twitter         = db.StringProperty()
    contact_email   = db.EmailProperty()
    updated         = db.DateTimeProperty()
    
class FeedReference(db.Model):
    date_last_updated = db.FloatProperty()
    feed_baseurl      = db.LinkProperty()
    name              = db.StringProperty()
    area              = db.StringProperty()
    url               = db.LinkProperty()
    country           = db.StringProperty()
    dataexchange_url  = db.LinkProperty()
    state             = db.StringProperty()
    license_url       = db.LinkProperty()
    date_added        = db.FloatProperty()