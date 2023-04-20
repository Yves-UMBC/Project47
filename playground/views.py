# Contains functions and classes that handle what data is displayed in the HTML templates

from django.shortcuts import render
from django.http import HttpResponse

# The home page of the crime map
def crime_map_index(request):
    return render(request, 'crime_map_index.html')

# Rednering visualization page
def visual_option(request):
    return render(request, 'visual_option.html')