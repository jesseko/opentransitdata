from google.appengine.ext import db
# from django.contrib.auth.models import get_hexdigest, check_password

class PetitionModel(db.Model):
    name        = db.StringProperty()
    email       = db.EmailProperty()
    city        = db.StringProperty()
    state       = db.StringProperty()
    country     = db.StringProperty()
    
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
    phone           = db.StringProperty()
    
class FeedReference(db.Model):
    """feed reference models a GTFS Data Exchange entity"""
    
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
    
class TransitAppStats(db.Model):
    # low contention model -- don't bother with sharding
    transit_app_count   = db.IntegerProperty()
    
    @staticmethod
    def get_transit_app_stats():
        # A "singleton" datastore entry for now
        stats = TransitAppStats.all().get()
        if stats is None:
            stats = TransitAppStats(transit_app_count = 0)
            try:
                stats.put()
            except db.TimeoutException:
                stats.put()
            
    @staticmethod
    def get_transit_app_count():
        return TransitAppStats.get_transit_app_stats().transit_app_count
        
    @staticmethod
    def increment_transit_app_count():
        stats = TransitAppStats.get_transit_app_stats()
        stats.transit_app_count = stats.transit_app_count + 1
        try:
            stats.put()
        except db.TimeoutException:
            stats.put()
    
class TransitApp(db.Model):
    slug                = db.StringProperty(indexed=True)
    title               = db.StringProperty()
    description         = db.StringProperty()
    url                 = db.LinkProperty()
    author_name         = db.StringProperty()
    author_email        = db.EmailProperty()
    long_description    = db.TextProperty()
    tags                = db.StringListProperty()
    screen_shot         = db.BlobProperty()
    