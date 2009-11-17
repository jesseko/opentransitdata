import time
import logging
from google.appengine.ext import db
from ..forms import PetitionForm, AgencyForm, AddAppForm
from ..utils.view import render_to_response, redirect_to, not_implemented
from ..models import FeedReference, Agency

def home(request):    
    new_refs = FeedReference.all().order("-date_added")
    petition_form = PetitionForm()    
    agencies = Agency.all()
    return render_to_response(request, 'home.html', {'petition_form':petition_form, 'new_refs': new_refs, 'agencies':agencies})
    
