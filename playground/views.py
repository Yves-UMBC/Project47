# Contains functions and classes that handle what data is displayed in the HTML templates

from django.shortcuts import render
from django.http import HttpResponse
from .models import Crime, Neighborhood

# The home page of the crime map


def crime_map_index(request):
    crimelist = Crime.objects.all()
    neighborhoodlist = Neighborhood.objects.values("name").distinct().order_by("name")
    weaponlist = Crime.objects.values("weapon").distinct().order_by("weapon")
    descriptionlist = Crime.objects.values("description").distinct().order_by("description")
    crimecodelist = Crime.objects.values("crimecode").distinct().order_by("crimecode")
    context = {
        "crimelist": crimelist,
        "neighborhoodlist": neighborhoodlist,
        "weaponlist": weaponlist,
        "descriptionlist": descriptionlist,
        "crimecodelist": crimecodelist,
    }
    return render(request, 'crime_map_index.html', context)

# Rednering visualization page


def visual_option(request):
    return render(request, 'visual_option.html')
