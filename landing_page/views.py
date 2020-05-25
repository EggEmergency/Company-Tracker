from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import F, Sum, FloatField, Count

from .models import Company

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
    #allLocations = Company.objects.order_by().values('location').distinct()
    allLocations = Company.objects.all().annotate(count=Count('location')).order_by('count').values('location').distinct()

    locations = []
    for loc in allLocations:
        locations.append(loc['location'])
        
    geoLocation = locations[0]
    if "location" in request.GET:
        geoLocation = request.GET["location"]

    #pdb.set_trace()

    workingCompanies = Company.objects.filter(location__exact=geoLocation)
    compStat = workingCompanies.aggregate(
        weightedAvg = Sum(F('rating')*F('reviewCount'), output_field=FloatField()) / 
            Sum(F('reviewCount'), output_field=FloatField()))


    weighting = 10
    if "weight" in request.GET:
        weighting = int(request.GET["weight"])

    for comp in workingCompanies:
        comp.weightedRating = (comp.rating*comp.reviewCount + weighting*compStat["weightedAvg"])\
            / (comp.reviewCount + weighting)
        pass

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
