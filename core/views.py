from django.http import HttpResponse
from django.shortcuts import render_to_response

def stub(request):
    name = request.GET['name']
    
    return render_to_response( "stub.html", {'name':name} )