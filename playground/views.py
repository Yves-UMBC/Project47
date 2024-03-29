# Contains functions and classes that handle what data is displayed in the HTML templates
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.contrib import messages
from .models import Crime, Neighborhood


# The home page of the crime map
def crime_map_index(request):
    crimelist = 0
    neighborhoods = get_data(request, "neighborhood")
    weapons = get_data(request, "weapon")
    descriptions = get_data(request, "description")
    crimecodes = get_data(request, "crimecode")
    dates = get_date_data(request)

    # retrieving the existing charts from the session or create an empty list
    charts = request.session.get('charts', [])

    if request.method == 'POST':
        # retrieving the chart request from the chart-preview page
        if ('chart-type' in request.POST) and ('chart-data' in request.POST):
            # retrieving the chart's type and crime data as a str
            chart_type = request.POST.get('chart-type')
            chart_data = request.POST.get('chart-data')

            charts.append({'chart_type': chart_type, 'chart_data': chart_data})

            # update the session
            request.session['charts'] = charts

    if 'weapon' in request.POST and None not in weapons:
        crimelist = Crime.objects.filter(neighborhood__in=neighborhoods, description__in=descriptions, datetime__gte=dates[0], datetime__lte=dates[1], crimecode__in=crimecodes).filter(weapon__in=weapons)
    else:
        crimelist = Crime.objects.filter(neighborhood__in=neighborhoods, description__in=descriptions, datetime__gte=dates[0], datetime__lte=dates[1], crimecode__in=crimecodes).filter(Q(weapon__in=weapons) | Q(weapon__isnull=True))

    print("Num of crimes", len(crimelist))
    if len(crimelist) == 0:
        messages.add_message(request, messages.WARNING, "No Results Found")

    neighborhoodlist = Neighborhood.objects.values("name").distinct().order_by("name")
    weaponlist = Crime.objects.values("weapon").distinct().order_by("weapon")
    descriptionlist = Crime.objects.values("description").distinct().order_by("description")
    crimecodelist = Crime.objects.values("crimecode").distinct().order_by("crimecode")
    recentcrimes = list(Crime.objects.order_by('-datetime')[:100])
    context = {
        "crimelist": crimelist,
        "neighborhoodlist": neighborhoodlist,
        "weaponlist": weaponlist,
        "descriptionlist": descriptionlist,
        "crimecodelist": crimecodelist,
        "recentcrimes": recentcrimes,
        "charts": charts, # hold a dictionary value for chart_type and chart_crime_data
    }
    return render(request, 'crime_map_index.html', context)


# function used to delete chart
def delete_chart(request):
    print("inside delete chart")
    id = request.GET.get("param1")
    charts = request.session.get('charts', [])
    
    charts.pop(int(id))

    request.session['charts'] = charts
    request.session.modified = True
    
    return JsonResponse({'charts': charts})

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

# This view function handle neighborhood data from the visual_option.html page
def get_neighborhood_data(request):
    displayData = {
        "dataLabels": [],
        "dataCounts": [],
    }
    return JsonResponse(displayData) 

# return the date range for the crimes to be displayed on the map
# based on user input from the filter options
# default dates are based on the earilest and latest crimes in the Crime table
def get_date_data(request):
    dates = []
    # get the earliest and latest crime dates from the Crime table
    datesTemp = Crime.objects.values_list("datetime", flat=True).distinct().order_by("datetime")
    dates.append(datesTemp[0])
    dates.append(datesTemp[len(datesTemp) - 1])

    if 'startDate' or 'endDate' in request.POST: # user gave date to filter by
        startFlag = 0
        start = request.POST.get('startDate')
        end = request.POST.get('endDate')
        if start:
            startFlag = 1
        # check that user start date is valid (in the crime table)
        if start:
            start = start.replace("-", "/")
            start = start + " 00:00:00+00"
            if start[:10] < dates[0][:10] or start[:10] > dates[1][:10]:
                start = dates[0]
                messages.add_message(request, messages.WARNING, "Invalid Start Date: Set to " + start[:10])
        else:
            start = dates[0]
            if end:
                messages.add_message(request, messages.WARNING, "No Start Date Given: Set to " + start[:10])

        # check that user end date is valid (in the crime table)
        if end:
            end = end.replace("-", "/")
            end = end + " 99:99:99+99"
            if end[:10] > dates[1][:10] or end[:10] < dates[0][:10]:
                end = dates[1]
                messages.add_message(request, messages.WARNING, "Invalid End Date: Set to " + end[:10])
        else:
            end = dates[1]
            if startFlag:
                messages.add_message(request, messages.WARNING, "No End Date Given: Set to " + end[:10])

        # user inputs end date that is before start date
        if end[:10] < start[:10]:
            end = dates[1]
            messages.add_message(request, messages.WARNING, "Invalid End Date: Set to " + end[:10])
            
        dates[0] = start
        dates[1] = end
    return dates

# return the list of values for the attribute 'type' to pull crime data from
# 'type' is a str that matches a column in the Crime table
def get_data(request, type):
    if type in request.POST and request.POST.get(type) != 'None': # user gave a filter for 'type'
        return request.POST.getlist(type)
    return Crime.objects.values_list(type, flat=True).distinct().order_by(type)
