__author__ = 'jeremydyer'
import requests
import re
from bs4 import BeautifulSoup

#globals
url = "http://www.vtinfo.com/PF/product_finder.asp"
custID = "NHB"
a = "view"

def listBeers():

    # Get the information about the current user that is needed.
    payload = {'custID': custID}
    resp = requests.post(url=url, data=payload)

    return getListOfBeersFromResponse(resp)

def getListOfBeersFromResponse(response):
    soup = BeautifulSoup(response.text)
    res = soup('select', {'name': 'b'})
    beers = []

    for beer in res:
        bs = beer.find_all('option')
        for b in bs:
            beers.append(b.text)

    return beers

def buildAddress(addressTag):
    address = ''
    for add in addressTag.contents:
        try:
            if len(add.contents) > 0:
                address = address + buildAddress(add)
            else:
                address = address + " " + add
        except AttributeError:
            address = address + " " + add

    return address

def findBrandsAtLocation(location):
    brandsRoot = location.find('ul').find('li').contents
    brandsList = recursiveBuildList(brandsRoot)
    return brandsList

#Recursivly builds a list of nested elements from the root
def recursiveBuildList(root):
    list = []
    for element in root:
        try:
            list.extend(recursiveBuildList(element.contents))
        except AttributeError:
            list.append(element.replace('\r', '').replace('\n', '').replace('\t', '').strip())
    return list

def findNewHollandBeers(lat, long, specificDrinkSearchingFor, includeBars, searchRadius, townStateZip):

    # Get the information about the current user that is needed.
    payload = {'custID': custID, 'a': a, 'lat': lat, 'long': long, 'b': specificDrinkSearchingFor, 't': includeBars, 'm': searchRadius, 'd': townStateZip}
    resp = requests.post(url=url, data=payload)

    soup = BeautifulSoup(resp.text)
    res = soup('tr', {'class': re.compile(r"finder_row_*", re.IGNORECASE)}) #Locate all rows with class 'finder_row_a' or 'finder_row_b'
    results = []
    for searchResult in res:
        finderDba = searchResult.find('td', {'class': 'finder_dba'}).text.replace(u'\u00a0', ' ')
        finderAddress = buildAddress(searchResult.find('td', {'class': 'finder_address'})).replace(u'\u00a0', ' ')
        finderPhone = searchResult.find('td', {'class': 'finder_phone'}).text.replace(u'\u00a0', ' ')
        finderMiles = searchResult.find('td', {'class': 'finder_miles'}).text.replace(u'\u00a0', ' ')

        #Gets all of the brands that are available at this location
        brandsAvailable = findBrandsAtLocation(searchResult)

        searchResult = {'dba': finderDba, 'address': finderAddress, 'phone': finderPhone, 'miles': finderMiles, 'brands': brandsAvailable}
        results.append(searchResult)

    responsePayload = {'beer_list': getListOfBeersFromResponse(resp), 'search_results': results}

    return responsePayload

#Uncomment for command line debugging and view results
print findNewHollandBeers("33.7924600000", "-84.3404030000", "", "off", "15", "Druid Hills, GA 30306")