from .forms import PetitionForm
from .utils import render_to_response, redirect_to, not_implemented, login_required
from .models import PetitionModel, FeedReference, Agency
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson as json
from google.appengine.ext import db
from google.appengine.ext.db import Key

def home(request):    
    new_refs = FeedReference.all().order("-date_added")
    petition_form = PetitionForm()
    
    return render_to_response(request, 'home.html', {'petition_form':petition_form, 'new_refs': new_refs})
    
def example_petition_form(request):
    # This example page handles the petition form!
    # This is how you typically handle forms in Django.
    # Again, it is only an example!    
    
    if request.method == 'POST':
        form = PetitionForm(request.POST)
        if form.is_valid():
            model = PetitionModel()
            model.name = form.cleaned_data['name']
            model.email = form.cleaned_data['email']
            model.city = form.cleaned_data['city']
            model.state = form.cleaned_data['state']
            model.country = form.cleaned_data['country']
            model.put()
            return redirect_to('example_petition_success')
    else:
        form = PetitionForm()
        
    return render_to_response(request, 'example_petition_form.html', {'form': form})

def example_petition_success(request):
    return render_to_response(request, 'example_petition_success.html')

from google.appengine.api.urlfetch import fetch
import logging
def replace_feed_references(old_references, new_references):
    # TODO: deleting one at a time is stupid
    # delete all current references
    for feed_reference in old_references:
        feed_reference.delete()
    
    # add all the new references
    parentKey = Key.from_path("FeedReference", "base")
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
    feed_refs_json = json.loads( fetch( FEED_REFS_URL ).content )['data']
    
    # replace feed references in a transaction
    old_references = FeedReference.all().fetch(1000)
    db.run_in_transaction(replace_feed_references, old_references, feed_refs_json)
      
    # redirect to a page for viewing all your new feed references
    return HttpResponseRedirect( "feed_references" )
    
def pretty_print_time_elapsed(float_time):
    return "%d days %d hours" %(float_time/(3600*24),(float_time%(3600*24))/3600)
    
import time
def feed_references(request):
    all_references = FeedReference.all().order("-date_added")
    
    refs_with_elapsed = []
    present_moment = time.time()
    for ref in all_references:
        refs_with_elapsed.append( {'ref':ref, 'ago':pretty_print_time_elapsed(present_moment-ref.date_added)} )
    
    return render_to_response( request, "feed_references.html", {'all_references':refs_with_elapsed} )
    
def agencies(request):
    
    agencies = Agency.all().order('state').order('city').order('name')
    
    return render_to_response( request, "agencies.html", {'agencies':agencies} )
    
def agency(request, agency_id):
    agency = Agency.get_by_id( int(agency_id) )
    
    return render_to_response( request, "agency.html", {'agency':agency} )