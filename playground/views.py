# Contains functions and classes that handle what data is displayed in the HTML templates
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from .models import Crime, Neighborhood


# The home page of the crime map
def crime_map_index(request):
    # del request.session['charts']
    crimelist = 0
    if request.method == 'POST':
        print(f"\n\nINSIDE OF request.POST", request.POST, "\n\n") ########### TEST
        neighborhoods = []
        weapons = []
        descriptions = []
        crimecodes = []

        # retrieving the chart request from the chart-preview page
        if ('chart-type' in request.POST) and ('chart-crime-data' in request.POST):
            # storing the chart request values
            chart_type = request.POST.get('chart-type')
            chart_crime_data = request.POST.get('chart-crime-data')
            # retrieving the existing charts from the session or create an empty list
            charts = request.session.get('charts', [{}])

            print("\n\nAFTER request.session.get", charts, "\n\n") ######### TEST

            set_chart = charts[0] # {}
            if 'chart-type' in set_chart and 'chart-crime-data' in set_chart:
                set_chart['chart_type'] = set_chart['chart_type'].extend(chart_type)
                set_chart['chart_crime_data'] = set_chart['chart_crime_data'].extend(chart_crime_data)
            else:
                set_chart['chart_type'] = chart_type
                set_chart['chart_crime_data'] = chart_crime_data

            charts[0] = set_chart

            print("\n\nAFTER charts.append", charts, "\n\n") ######### TEST

            request.session['charts'] = charts

            print("\n\nAFTER request.session['charts']", request.session['charts'], "\n\n") ######### TEST

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
            # "charts": charts, # hold a dictionary value for chart_type and chart_crime_data
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
        # "charts": charts, # hold a dictionary value for chart_type and chart_crime_data
    }
    return render(request, 'crime_map_index.html', context)

# helper function for crime_map_index to help rendering the charts
def chart_rendering():
    pass


# Rendering visualization page
def visual_option(request):
    crimelist = Crime.objects.all()
    neighborhoodlist = Neighborhood.objects.all()
    context = {
        "crimelist": crimelist,
        "neighborhoodlist": neighborhoodlist,
    }
    return render(request, 'visual_option.html', context)

# sending Json request over to the chart_script.js
def get_crime_data(request):
    queryType = request.GET.get("param1")

    # queryList is querySets of all Crime data filter by queryType
    crimeList = Crime.objects.all().values(queryType)
    dataDict = {}

    # queryValues is a dictionary (Ex: {'weapon': "PERSONAL_WEAPON"})
    for crimeDict in crimeList:
        dataType = crimeDict[queryType]
        dataDict[dataType] = dataDict.get(dataType, 0) + 1

    displayData = {
        "dataLabels": list(dataDict.keys()),
        "dataCounts": list(dataDict.values()),
    }
    return JsonResponse(displayData)

def get_neighborhood_data(request):
    # Already created a path for this views function
    pass