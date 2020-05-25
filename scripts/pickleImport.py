import pickle
from landing_page.models import Company

inFile = open("torontoCompanies.dump", "rb")
parsedCompanies = pickle.load(inFile)

for parsedComp in parsedCompanies:
    newCompany = Company()
    newCompany.name = parsedComp.name.lower()
    newCompany.website = parsedComp.website.lower()
    newCompany.reviewCount = parsedComp.reviews
    newCompany.interviewCount = parsedComp.interviews
    newCompany.salaryCount = parsedComp.salaries
    newCompany.recommendedPercent = parsedComp.recommended
    newCompany.rating = parsedComp.rating
    newCompany.location = parsedComp.location

    if newCompany.reviewCount == None:
        newCompany.reviewCount = 0

    if newCompany.interviewCount == None:
        newCompany.interviewCount = 0

    if newCompany.salaryCount == None:
        newCompany.salaryCount = 0

    if Company.objects.filter(name=newCompany.name).exists():
        pass
    else:
        newCompany.save()
