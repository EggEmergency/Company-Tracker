from landing_page.models import Company

allComp = Company.objects.all()
for comp in allComp:
    comp.location = "San Francisco, CA"
    comp.save()
