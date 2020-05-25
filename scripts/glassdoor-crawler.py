import bs4
import requests
import re
import pickle
import time
import sys

from landing_page.models import Company, Location


"""
parse_companies
    soupedHTML - the web page which has been put through beautifulsoup4
    givenLocation - the city which we are searching, a reference to a database row
"""
def parse_companies(soupedHTML, givenLocation):
    companiesHTML = soupedHTML.findAll("div", class_=re.compile("empInfo"))

    for companyHTML in companiesHTML:
        companyInfo = companyHTML.parent


        # Data acquiring and cleaning 
        # NAME
        try:
            companyName = companyInfo.find("div", class_=re.compile("margBot")).get_text()
            companyName = companyName.strip()
        except:
            companyName = "N/A"

        # WEBSITE
        try:
            companyWebsite = companyInfo.find("span", class_="url").get_text()
        except:
            companyWebsite = "N/A"

        # REVIEWS
        try:
            reviews = companyInfo.find("a", class_=re.compile("reviews"))
            companyReviews = reviews.find("span", class_=re.compile("num")).get_text()
            companyReviews = companyReviews.strip()
            companyReviews = string_to_number(companyReviews)
        except:
            companyReviews = 0

        # SALARIES
        try:
            salaries = companyInfo.find("a", class_=re.compile("salaries"))
            companySalaries = salaries.find("span", class_=re.compile("num")).get_text()
            companySalaries = companySalaries.strip()
            companySalaries = string_to_number(companySalaries)
        except:
            companySalaries = 0

        # INTERVIEWS
        try:
            interviews = companyInfo.find("a", class_=re.compile("interviews"))
            companyInterviews = interviews.find("span", class_=re.compile("num")).get_text()
            companyInterviews = companyInterviews.strip()
            companyInterviews = string_to_number(companyInterviews)
        except:
            companyInterviews = 0

        # RECOMMENDED
        try:
            recommended = companyInfo.find(text=re.compile("recommended.*friend"))
            companyRecommended = recommended
            companyRecommended = companyRecommended.split()[0]
            companyRecommended = companyRecommended.strip()
            companyRecommended = companyRecommended[:-1]
            companyRecommended = string_to_number(companyRecommended)
        except:
            companyRecommended = 0

        # RATINGS
        try:
            rating = companyInfo.find("span", class_=re.compile("Rating"))
            companyRating = rating.get_text()
            companyRating = float(companyRating)
        except:
            companyRating = 0

        print(companyName)
        print("Site:", companyWebsite)
        print("Reviews:", companyReviews)
        print("Salaries:", companySalaries)
        print("Interviews:", companyInterviews)
        print("Rating:", companyRating)
        print("Recommend:", companyRecommended)
        print()

        try:
            currCompany = Company.objects.get(name=companyName)
        except:
            currCompany = Company()
            currCompany.name = companyName
        currCompany.website = companyWebsite
        currCompany.reviewCount = companyReviews
        currCompany.salaryCount = companySalaries
        currCompany.interviewCount = companyInterviews
        currCompany.rating = companyRating
        currCompany.recommendedPercent = companyRecommended
        currCompany.save()
        currCompany.locations.add(givenLocation)

"""
Glassdoor keeps track of its metrics as:
    3.3k = 3300
    983 = 983
    No millions yet, but we'll see
"""
def string_to_number(inputStr):
    if inputStr[-1].isnumeric():
        return int(inputStr)
    else:
        if inputStr[-1] == "k":
            newStr = inputStr[:-1]
            ret = float(newStr)*1000
            return int(ret)


"""
Find the link to the next page
GET the next page
Return said page
"""
def next_page(soupedHTML):
    nextObject = soupedHTML.find("li", class_="next")
    if nextObject == None:
        return None
    if nextObject.find("a"):
        retURL = nextObject.find("a")["href"]
    else:
        retURL = None
    return retURL

# MAIN FUNCTION
def run(*args):
# Setup session to perform rest requests
    reqSession = requests.session()
    getCookies = reqSession.get("https://glassdoor.com")
    cookies = getCookies.cookies
    baseURL = 'https://www.glassdoor.ca'

# Accept the city as a commandline argument
    city = args[0]

# Vancouver
    if city == "VancouverBC":
        url = 'https://www.glassdoor.ca/Reviews/vancouver-software-engineer-reviews-SRCH_IL.0,9_IM972_KO10,27.htm'
        locale = Location.objects.get(name="Vancouver, BC")

# Montreal
    elif city == "MontrealQC":
        url = 'https://www.glassdoor.ca/Reviews/montreal-software-engineer-reviews-SRCH_IL.0,8_IM990_KO9,26.htm'
        locale = Location.objects.get(name="Montreal, QC")

# Toronto
    elif city == "TorontoON":
        url = 'https://www.glassdoor.ca/Reviews/toronto-software-engineer-reviews-SRCH_IL.0,7_IM976_KO8,25.htm'
        locale = Location.objects.get(name="Toronto, ON")

# San Francisco
    elif city == "SanFranciscoCA":
        url = 'https://www.glassdoor.ca/Reviews/san-francisco-software-engineer-reviews-SRCH_IL.0,13_IM759_KO14,31.htm'
        locale = Location.objects.get(name="San Francisco, CA")

# Ottawa as a test case, way less companies, easier test
    elif city == "OmegalulON":
        url = 'https://www.glassdoor.ca/Reviews/ottawa-software-engineer-reviews-SRCH_IL.0,6_IM981_KO7,24.htm'
        locale = Location.objects.get(name="omegalul, CA")

    else:
        print("IMPROPER ARGUMENT USAGE")
        return
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    last_page = False
    iterURL = url
    pageCounter = 0
    while iterURL != None:
        response = reqSession.get(iterURL, headers=header, cookies=cookies)
        soup = bs4.BeautifulSoup(response.content, features='html.parser')
        parse_companies(soup, locale)
        iterURL = next_page(soup)
        if iterURL == None:
            break
        iterURL = baseURL + iterURL
        print(iterURL)
        time.sleep(0.05)

    print("Data written straight to database, baby!")
