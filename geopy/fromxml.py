#!/usr/bin/env python
# reads xml data
# created by : C0SM0

# imports
from bs4 import BeautifulSoup

# read data
page = open('maryland.kml', 'r').read()
soup = BeautifulSoup(page, "xml")

# iterate over kml
placemark = soup.find_all('Placemark')
for item in placemark:

    # get values
    name = item.find('name').text # name
    link = item.find('value').text # link
    coordinates = item.find('coordinates').text # coordinates

    # get longitude and latitude
    coordinates = coordinates.split(',')
    longitude = coordinates[0]
    latitude = coordinates[1]

    # diplay values
    print(name)
    print(link)
    print(longitude)
    print(latitude)
    print()
