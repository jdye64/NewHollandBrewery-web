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

    soup = BeautifulSoup(resp.text)
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
        searchResult = {'dba': finderDba, 'address': finderAddress, 'phone': finderPhone, 'miles': finderMiles}
        results.append(searchResult)

    return results