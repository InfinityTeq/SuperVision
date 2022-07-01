#!/usr/bin/env pyton
# london kml generator
# created by : C0SM0

# imports
import os
import json
import urllib.request
import xml.etree.ElementTree as ET

# values
read_file = open('cameras.json', 'r').read()
data = json.loads(read_file)

# account for ouptut
count = 1
output = ''

# iterate through each camera
for camera in data:

    # get values
    name = camera.get('name').replace('&', 'and')
    longitude = camera.get('lng')
    latitude = camera.get('lat')
    link = camera.get('image').replace('&', '&amp;')
    # link = camera.get('image')

    # write to placemark
    placemark = f'''
        <Placemark>
            <name>{name}</name>
            <styleUrl>#traffic_camera</styleUrl>
            <ExtendedData>
                <Data name="video">
                <value>{link}</value>
                </Data>
            </ExtendedData>
            <Point>
                <coordinates>{longitude},{latitude},0</coordinates>
            </Point>
        </Placemark>
    '''

    # save to output
    output += placemark

    # display count
    print(count)
    count += 1


# kml formats
kml_start = '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
<name>KmlFile</name>

<Style id="traffic_camera">
<IconStyle>
    <Icon>
    <href>https://cdn3.iconfinder.com/data/icons/world-top-cities-2-1/180/50-256.png</href>
    </Icon>
</IconStyle>
<BalloonStyle>
    <text>$[video]</text>
</BalloonStyle>
</Style>
'''

kml_end = '''
        </Document>
</kml>
'''

with open('washingtondc.kml', 'w') as kml:
    kml.write(kml_start + output + kml_end)
