from landing_page.models import Company

allComp = Company.objects.all()
for comp in allComp:
    print (comp.name)
