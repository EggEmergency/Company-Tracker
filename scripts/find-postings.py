import bs4
import requests
import re
import pickle
import time
import sys
import urllib.parse
import pdb
import collections

from landing_page.models import Company, Location


CAREER_REGEX = "(job|career|join|apply|opportunit)"

"""
Attempt a graph based depth-first search on the site

Loops are avoided by keeping track of urls visited

All urls on the front-page besides the job/careers link gets blacklisted to remove navbars, etc.

1) At the homepage:
    All of the links that are not related to a job are considered visited. This is to avoid clicking on unnecessary links: e.g. links in the navbar and footer, etc.

    Essentially, we only want to follow the links related to jobs when on the homepage

2)
Perform a breadth-first search using the jobs/ careers page as a starting point
"""
def run(*args):
    reqSession = requests.session()
    #allCompanies = Company.objects.all()
    #listingsRegex = "(apply|listings|join)"
    jobListRegex = ""
    visitedUrls = collections.defaultdict(lambda: 0)
    href = "href"

    for comp in Company.objects.all():
        url = comp.website
        url = "http://" + url
        baseUrl = url
        """
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        getCookies = reqSession.get(url)
        cookies = getCookies.cookies

        response = reqSession.get(url, headers=header, cookies=cookies)
        """
        try:
            response = requests.get(url)
            print(url)
        except:
            print("PROBLEM")
            print(url)
            continue
        soup = bs4.BeautifulSoup(response.content, features='html.parser')

        allLinks = soup.find_all('a')
        careerLinks = []
        for link in allLinks:
            if href in link.attrs:
                newUrl = link[href]
                linkText = link.get_text()
                joinedUrl = urllib.parse.urljoin(baseUrl, newUrl)
                if re.search(CAREER_REGEX, linkText, flags=re.IGNORECASE):
                    careerLinks.append(joinedUrl)
                else:
                    visitedUrls[joinedUrl] += 1
            else:
                pass

        print(careerLinks)

        for careerLink in careerLinks:
            BFS(careerLink, visitedUrls)
        print("WE ARE DONE AND WE ARE SLEEPING")
        time.sleep(10000)

"""
BFS - breadth-first search
    Parameters:
    rootURL - the root node at which we begin the breadth-first search
    visited - a dictionary of web pages which we visited to avoid loops

Performs a breadth-first search on the website from a specific starting point, and
automatically stops at a certain depth (it shouldn't take more than 3 clicks from the
jobs page to find the job listings)
"""
def BFS(rootUrl, visited):
    depth = 0
    href = "href"
    linkQueue = []
    linkQueue.append(rootUrl)
    linkQueue.append(None)

    while depth < 5 and len(linkQueue) > 0:
        currUrl = linkQueue.pop(0)
        if currUrl == None:
            depth += 1
            linkQueue.append(None)
        else:
            # DO THE THING
            print("url:", currUrl)
            print("depth:", depth)
            try:
                response = requests.get(currUrl)
            except:
                pass
            currSoup = bs4.BeautifulSoup(response.content, features='html.parser')
            neighbourLinks = currSoup.find_all('a')
            for neighbourLink in neighbourLinks:
                if href in neighbourLink.attrs:
                    neighbourUrl = neighbourLink[href]
                    joinedUrl = urllib.parse.urljoin(currUrl, neighbourUrl)
                    if re.search(CAREER_REGEX, joinedUrl, flags=re.IGNORECASE):
                        if joinedUrl not in visited:
                            visited[joinedUrl] += 1
                            linkQueue.append(joinedUrl)
                        else:
                            pass
                else:
                    pass
