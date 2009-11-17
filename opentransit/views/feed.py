import time
import logging
from django.utils import simplejson as json
from google.appengine.ext import db
from google.appengine.api.urlfetch import fetch as fetch_url
from ..utils.view import render_to_response, redirect_to, not_implemented
from ..utils.prettyprint import pretty_print_time_elapsed
from ..models import FeedReference

def replace_feed_references(old_references, new_references):
    # TODO: deleting one at a time is stupid
    # delete all current references
    for feed_reference in old_references:
        feed_reference.delete()
    
    # add all the new references
    parentKey = db.Key.from_path("FeedReference", "base")
    for feed_reference_json in new_references:
        fr = FeedReference(parent=parentKey)
        fr.date_last_updated = feed_reference_json['date_last_updated']
        fr.feed_baseurl      = feed_reference_json['feed_baseurl'].strip() if feed_reference_json['feed_baseurl'] != "" else None
        fr.name              = feed_reference_json['name']
        fr.area              = feed_reference_json['area']
        fr.url               = feed_reference_json['url'].strip()
        fr.country           = feed_reference_json['country']
        fr.dataexchange_url  = feed_reference_json['dataexchange_url'].strip()
        fr.state             = feed_reference_json['state']
        fr.license_url       = feed_reference_json['license_url'].strip() if feed_reference_json['license_url'] != "" else None
        fr.date_added        = feed_reference_json['date_added']
        fr.put()

def update_feed_references(request):
    FEED_REFS_URL = "http://www.gtfs-data-exchange.com/api/agencies"
    
    # grab feed references and load into json
    feed_refs_json = json.loads( fetch_url( FEED_REFS_URL ).content )['data']
    
    # replace feed references in a transaction
    old_references = FeedReference.all().fetch(1000)
    db.run_in_transaction(replace_feed_references, old_references, feed_refs_json)
      
    # redirect to a page for viewing all your new feed references
    return redirect_to("feed_references")
    
def feed_references(request):
    all_references = FeedReference.all().order("-date_added")
    
    refs_with_elapsed = []
    present_moment = time.time()
    for ref in all_references:
        refs_with_elapsed.append( {'ref':ref, 'ago':pretty_print_time_elapsed(present_moment-ref.date_added)} )
    
    return render_to_response( request, "feed_references.html", {'all_references':refs_with_elapsed} )

