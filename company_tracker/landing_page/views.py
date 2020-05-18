from django.shortcuts import render
from django.http import HttpResponse

from .models import Company
def landing(request):
    allCompanies = Company.objects.all()
    context = {
        'company_list': allCompanies,
    }
    return render(request, 'landing_page.html', context)

def about(request):
    return render(request, 'about.html')

def analysis(request):
    return render(request, 'analysis.html')

def leaderboards(request):
    return render(request, 'leaderboards.html')
