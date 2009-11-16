from django import forms
from django.forms import ModelForm
from .models import PetitionModel, Agency

# NOTE DAVEPECK: this is an example only. Ignore as you see fit!

class PetitionForm(forms.Form):  
    name = forms.CharField(max_length = 128, min_length = 6, label = u"Name")
    email = forms.EmailField(label = u"Email")
    city = forms.CharField(max_length = 64, min_length = 3, label = u"City")
    state = forms.CharField(max_length = 16, min_length = 2, label = u"State")
    country = forms.CharField(max_length = 16, min_length = 2, label = u"Country")

class AddAppForm(forms.Form):
    title = forms.CharField(max_length = 64, min_length = 6, label = u"Title")
    description = forms.CharField(max_length = 140, min_length = 6, label = u"One Sentence Description")
    url = forms.URLField(verify_exists = False, min_length = 6, label = u"App URL")
    author_name = forms.CharField(max_length = 128, min_length = 6, label = u"Author's Name")
    author_email = forms.EmailField(label = u"Author's Email (kept private)")
    long_description = forms.CharField(min_length = 0, max_length = 2048, widget = forms.widgets.Textarea(attrs = {'rows': 6, 'cols': 32}), label = u"Extended Description")
    tags = forms.CharField(max_length = 256, min_length = 0, label = u"Tags (comma separated)")
    screen_shot = forms.ImageField(label = u"Screen Shot (optional)")
        
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
