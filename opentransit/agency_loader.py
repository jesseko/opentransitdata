import datetime
from google.appengine.ext import db
from google.appengine.tools import bulkloader
import models

class AgencyLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'Agency',
                                   [('name', str),
                                    ('short_name', str),
                                    ('city', str),
                                    ('state', str),
                                    ('executive', str),
                                    ('contact_email',str),
                                    ('agency_url', lambda x: str(x) if x is not None and x!="" else None),
                                    ('phone', str),
                                    ('address', str),
                                   ])

loaders = [AgencyLoader]