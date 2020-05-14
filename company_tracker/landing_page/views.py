from django.shortcuts import render
from django.http import HttpResponse

from .models import Company
def landingView(request):
    """
    allCompanies = Company.objects.all()
    context = {
        'company_list': allCompanies,
    }
    return render(request, 'landing_page.html', context)
    """
    return HttpResponse("LandingView baby")
