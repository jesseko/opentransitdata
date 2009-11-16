from django import forms
from django.forms import ModelForm
from .models import PetitionModel, Agency

# NOTE DAVEPECK: this is an example only. Ignore as you see fit!

class PetitionForm(forms.Form):  
    name = forms.CharField(max_length=128, min_length=6, label=u"Name")
    email = forms.EmailField(label=u"Email")
    city = forms.CharField(max_length=64, min_length=3, label=u"City")
    state = forms.CharField(max_length=16, min_length=2, label=u"State")
    country = forms.CharField(max_length=16, min_length=2, label=u"Country")
    
class AgencyForm(forms.Form):
    name            = forms.CharField()
    short_name      = forms.CharField(required=False)
    tier            = forms.IntegerField(required=False)
    city            = forms.CharField(required=False)
    state           = forms.CharField(max_length=2,required=False)
    country         = forms.CharField(required=False)
    postal_code     = forms.IntegerField(required=False)
    address         = forms.CharField(required=False)
    agency_url      = forms.URLField(required=False)
    executive       = forms.CharField(required=False)
    executive_email = forms.EmailField(required=False)
    twitter         = forms.CharField(required=False)
    contact_email   = forms.EmailField(required=False)
    updated         = forms.DateTimeField(required=False)
    phone           = forms.CharField(required=False)