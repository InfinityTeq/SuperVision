#!/usr/bin/env pyton
# london kml generator
# created by : C0SM0

# imports
from opensky_api import OpenSkyApi

def get_flights():
    # values
    api = OpenSkyApi()
    data = api.get_states()

    # account for ouptut
    count = 0
    output = ''

    # iterate through each camera
    for plane in data.states:

        # get values
        name = plane.origin_country
        latitude = plane.latitude
        longitude = plane.longitude

        # filter out false positives
        if latitude == None or longitude == None:
            continue

        # write to placemark
        placemark = f'''
            <plane>
                <name>{name}</name>
                <lat>{latitude}</lat>
                <lon>{longitude}</lon>
            </plane>
        '''

        # save to output
        output += placemark

        # display count
        # print(count)
        count += 1

    # kml formats
    kml_start = '''<?xml version="1.0"?>
    '''

    return kml_start + output

    # with open('xml/plane-plane-AirPlane-0-1-2.xml', 'w') as kml:
    #     kml.write(kml_start + output)
