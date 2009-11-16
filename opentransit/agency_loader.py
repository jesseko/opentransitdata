import datetime
from google.appengine.ext import db
from google.appengine.tools import bulkloader
import models

class AgencyLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'Agency',
                                   [('long_name', str),
                                    ('short_name', str),
                                    ('area', str),
                                    ('state', str),
                                    ('contact', str),
                                    ('url', str),
                                    ('phone', str),
                                    ('address', str),
                                   ])

exporters = [AgencyLoader]