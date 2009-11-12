from django import forms
from .models import ExamplePetitionModel

# NOTE DAVEPECK: this is an example only. Ignore as you see fit!

class ExamplePetitionForm(forms.Form):  
    name = forms.CharField(max_length=128, min_length=6, label=u"Name")
    email = forms.EmailField(label=u"Email")
    city = forms.CharField(max_length=64, min_length=3, label=u"City")
    state = forms.CharField(max_length=16, min_length=2, label=u"State")
    country = forms.CharField(max_length=16, min_length=2, label=u"Country")
    
