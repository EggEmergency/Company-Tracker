import pickle
from landing_page.models import Company

inFile = open("SanFran.dump", "rb")
parsedCompanies = pickle.load(inFile)

for sfCompany in parsedCompanies:
    newCompany = Company()
    newCompany.name = sfCompany.name.lower()
    newCompany.website = sfCompany.website.lower()
    newCompany.reviewCount = sfCompany.reviews
    newCompany.interviewCount = sfCompany.interviews
    newCompany.salaryCount = sfCompany.salaries
    newCompany.recommendedPercent = sfCompany.recommended
    newCompany.rating = sfCompany.rating

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
