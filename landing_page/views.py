from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import F, Sum, FloatField, Count

from .models import Company
from .models import Location

import re
import pdb
"""
We query the database to deliver the data requested by the user.

1) User selects a location
    a) Default is the most populated one (San Francisco, usually)

2) Companies at that location are processed
    a) Weighted average is found
    b) Weighted rating is calculated for each company
"""
def landing(request):
    allLocations = Location.objects.all()
    locations = []
    for loc in allLocations:
        locations.append(loc.name)
        
    geoLocation = "San Francisco, CA"
    if "location" in request.GET:
        geoLocation = request.GET["location"]

    #pdb.set_trace()

    workingCompanies = Location.objects.get(name=geoLocation).companies.all()
    #pdb.set_trace()
    compStat = workingCompanies.aggregate(
        weightedAvg = Sum(F('rating')*F('reviewCount'), output_field=FloatField()) / 
            Sum(F('reviewCount'), output_field=FloatField()))


    weighting = 10
    if "weight" in request.GET:
        weighting = int(request.GET["weight"])

    for comp in workingCompanies:
        if comp.rating == None or comp.reviewCount == None:
            comp.weightedRating = None
        else:
            comp.weightedRating = (comp.rating*comp.reviewCount + weighting*compStat["weightedAvg"])\
                / (comp.reviewCount + weighting)
        
    context = {
        'company_list': workingCompanies,
        'weighting': weighting,
        'locations': locations,
        'currentLocation': geoLocation,
    }
    return render(request, 'landing_page.html', context)

def about(request):
    return render(request, 'about.html')

def analysis(request):
    return render(request, 'analysis.html')

def leaderboards(request):
    return render(request, 'leaderboards.html')
