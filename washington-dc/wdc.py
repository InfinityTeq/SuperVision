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
count = 0
output = ''

# iterate through each camera
for camera in data:

    # get values
    name = camera.get('commonName').replace('&', 'and')
    cam_id = camera.get('id').replace('JamCams_','')
    longitude = camera.get('lon')
    latitude = camera.get('lat')

    # format values
    link = f'https://www.hlsplayer.net/mp4-player#src=https%3A%2F%2Fs3-eu-west-1.amazonaws.com%2Fjamcams.tfl.gov.uk%2F{cam_id}.mp4'

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
    <href>https://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
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

with open('london.kml', 'w') as kml:
    kml.write(kml_start + output + kml_end)
