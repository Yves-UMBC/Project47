# Contains functions and classes that handle what data is displayed in the HTML templates

from django.shortcuts import render
from django.http import HttpResponse
from .models import Crime

# The home page of the crime map
def crime_map_index(request):
    crimelist = Crime.objects.all()
    return render(request, 'crime_map_index.html', {'crimelist' : crimelist})

# Rednering visualization page
def visual_option(request):
    return render(request, 'visual_option.html')