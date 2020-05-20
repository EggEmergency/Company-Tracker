from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import F, Sum, FloatField

from .models import Company

def landing(request):
    allCompanies = Company.objects.all()
    compStat = Company.objects.all().aggregate(
        weightedAvg = Sum(F('rating')*F('reviewCount'), output_field=FloatField()) / 
            Sum(F('reviewCount'), output_field=FloatField()))

    weighting = 25
    if "weight" in request.GET:
        weighting = int(request.GET["weight"])

    for comp in allCompanies:
        comp.weightedRating = (comp.rating*comp.reviewCount + weighting*compStat["weightedAvg"])\
            / (comp.reviewCount + weighting)
        pass

    context = {
        'company_list': allCompanies,
        'weighting': weighting,
    }
    return render(request, 'landing_page.html', context)

def about(request):
    return render(request, 'about.html')

def analysis(request):
    return render(request, 'analysis.html')

def leaderboards(request):
    return render(request, 'leaderboards.html')
