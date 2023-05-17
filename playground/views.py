# Contains functions and classes that handle what data is displayed in the HTML templates

from django.shortcuts import render
from django.http import HttpResponse
from .models import Crime, Neighborhood
from django.db.models import Q
# The home page of the crime map


def crime_map_index(request):
    crimelist = 0
    if request.method == 'POST':
        neighborhoods = []
        weapons = []
        descriptions = []
        crimecodes = []
        if 'neighborhood' in request.POST:
            neighborhoods = request.POST.getlist('neighborhood')
        else:
            #neighborhoods = Neighborhood.objects.values_list("name", flat=True).distinct().order_by("name")
            neighborhoods = Crime.objects.values_list("neighborhood", flat=True).distinct().order_by('neighborhood')
        
        if 'weapon' in request.POST:
            weapons = request.POST.getlist('weapon')
        else:
            weapons = Crime.objects.values_list("weapon", flat=True).distinct().order_by("weapon")

        if 'description' in request.POST:
            descriptions = request.POST.getlist('description')
        else:
            descriptions = Crime.objects.values_list("description", flat=True).distinct().order_by("description")
        
        if 'crimecode' in request.POST:
            crimecodes = request.POST.getlist('crimecode')
        else:
            crimecodes = Crime.objects.values_list("crimecode", flat=True).distinct().order_by("crimecode")
            
    else:
        crimelist = Crime.objects.all()
        print("Start", len(crimelist))
        neighborhoodlist = Neighborhood.objects.values("name").distinct().order_by("name")
        weaponlist = Crime.objects.values("weapon").distinct().order_by("weapon")
        descriptionlist = Crime.objects.values("description").distinct().order_by("description")
        crimecodelist = Crime.objects.values("crimecode").distinct().order_by("crimecode")
        recentcrimes = Crime.objects.order_by('datetime')[:100]
        context = {
            "crimelist": crimelist,
            "neighborhoodlist": neighborhoodlist,
            "weaponlist": weaponlist,
            "descriptionlist": descriptionlist,
            "crimecodelist": crimecodelist,
            "recentcrimes" : recentcrimes,
        }
        return render(request, 'crime_map_index.html', context)

    #crimelist = Crime.objects.filter((Q(weapon__in=weapons) | Q(weapon__isnull=True)))
    crimelist = Crime.objects.filter(neighborhood__in=neighborhoods, description__in=descriptions, crimecode__in=crimecodes).filter(Q(weapon__in=weapons) | Q(weapon__isnull=True))
    print("modified", len(crimelist))
    neighborhoodlist = Neighborhood.objects.values("name").distinct().order_by("name")
    weaponlist = Crime.objects.values("weapon").distinct().order_by("weapon")
    descriptionlist = Crime.objects.values("description").distinct().order_by("description")
    crimecodelist = Crime.objects.values("crimecode").distinct().order_by("crimecode")
    recentcrimes = list(Crime.objects.order_by('datetime')[:100])
    print(len(recentcrimes))
    context = {
        "crimelist": crimelist,
        "neighborhoodlist": neighborhoodlist,
        "weaponlist": weaponlist,
        "descriptionlist": descriptionlist,
        "crimecodelist": crimecodelist,
        "recentcrimes" : recentcrimes,
    }
    return render(request, 'crime_map_index.html', context)

# Rendering visualization page


def visual_option(request):
    return render(request, 'visual_option.html')
