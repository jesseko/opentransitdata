import time
import logging
from google.appengine.ext import db

from ..forms import AddAppForm
from ..utils.view import render_to_response, redirect_to, not_implemented
from ..models import TransitApp, TransitAppStats

def app_gallery(request):
    # TODO davepeck
    pass
    
def app_details(request, transit_app_slug):
    # TODO davepeck
    pass
    
def app_screenshot(request, transit_app_slug):
    # TODO davepeck
    pass

def add_app_form(request):
    # TODO davepeck
    if request.method == 'POST':
        form = AddAppForm(request.POST, request.FILES)
        if form.is_valid():
            
            return redirect_to('home')
    else:
        form = AddAppForm()
        
    return render_to_response(request, 'add_app_form.html', {'form': form})
    
def add_app_success_form(request):
    # TODO davepeck
    pass

