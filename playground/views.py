# Contains functions and classes that handle what data is displayed in the HTML templates

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Crime, Neighborhood

# The home page of the crime map
def crime_map_index(request):
    crimelist = Crime.objects.all()
    context = {
        "crimelist": crimelist,
    }
    return render(request, 'crime_map_index.html', context)

# Rednering visualization page
def visual_option(request):
    # crimelist = Crime.objects.all()
    # neighborhoodlist = Neighborhood.objects.all()
    context = {
        # "crimelist": crimelist,
        # "neighborhoodlist": neighborhoodlist,
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