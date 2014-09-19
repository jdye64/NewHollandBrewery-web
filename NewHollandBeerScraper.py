__author__ = 'jeremydyer'
#Scraps the URL http://newhollandbrew.com/beer-finder/ for the complete list of NewHollands beers and produces a more
#software digestable JSON file which can be feed to the IOS app

import requests
import json
from bs4 import BeautifulSoup

baseUrl = "http://newhollandbrew.com"
scrapURL = "http://newhollandbrew.com/beer-finder/"

beers = []

def scrapIndividualBeer(url, beerBotteImageUrl):
    print "Getting URL " + url
    resp = requests.get(url=url)
    soup = BeautifulSoup(resp.text)
    item = soup.find('div', {'class': 'item active'})

    beer = {}
    print "\n"
    beerName = soup.find('a', {'class': 'breadcrumb', "href": "#"}).string
    print "BeerName -> " + beerName
    beer["BeerName"] = beerName
    beerLogoImageUrl = baseUrl + item.find('img', {'class': 'img-responsive logo'}).attrs['src']
    print "beerLogoImageUrl -> " + beerLogoImageUrl
    beer["BeerLogoImageURL"] = beerLogoImageUrl
    beer["BeerBottleImageURL"] = beerBotteImageUrl
    print "BeerBottleImageURL -> " + beerBotteImageUrl

    keys = soup.find_all('h6')
    values = soup.find_all('p')

    if len(keys) != len(values):
        print "EMERGENCY KEYS DO NOT MATCH THE NUMBER OF VALUES!!! DATA WILL BE WRONG!"
        return

    index = 0
    for key in keys:
        #print "Key -> " + str(key.string) + " Values -> " + str(values[index].string)
        beer[key.string] = values[index].string
        index += 1

    beers.append(beer)
    print "\n"

resp = requests.get(url=scrapURL)
soup = BeautifulSoup(resp.text)
resultList = soup.find('div', {'class': 'results-list'}).find('ul')

for result in resultList:
    findUrl = result.find('a')

    #Attempts to see if this h href contains a link
    try:
        href = findUrl.attrs["href"]
        beerBottleImageUrl = findUrl.find('img', {'class': 'img-responsive'}).attrs['src']
        scrapIndividualBeer(href, beerBottleImageUrl)
        href = ""
    except AttributeError:
        pass

print beers

f = open('./NewHollandBeers.json', 'w')
f.write(json.dumps(beers))
f.close()