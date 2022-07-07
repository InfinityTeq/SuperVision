#!/usr/bin/env python
# map all 50 states [automated]
# created by : C0SM0

# imports
import os
import json
import urllib.request
from bs4 import BeautifulSoup

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

# read state file
states = open('states.txt', 'r').readlines()

# map all 50 states
for state in states:

    # output kml
    output = ''

    # format state
    state = state.strip()
    print(state)

    # download html file
    os.system(f'wget https://www.traffic-cams.com/{state}/all')
    html = open('all', 'r').readlines()

    # file staging
    filename = state.lower()
    filepath_json = f'{filename}/{filename}.json'
    filepath_kml = f'../../kml/{filename}.kml'
    os.system(f'mkdir {filename}')
    start_writing = False

    # generate geojson file
    with open(filepath_json, 'w') as json_data:
        for line in html:

            # line formatting
            line = line.replace('OtherCamAnchor','""')
            line = line.replace('userPngIcon','""')

            # remove comments withou removing hyperlinks
            if '// ' in line:
                line = line[:line.index('// ')]

            # start writing to file
            if start_writing == False and ('		 ,{' in line):
                json_data.write('[{')
                start_writing = True
                continue

            # stop writing to file
            if line.startswith(' ]'):
                json_data.write(']')
                break

            # write line to file
            if start_writing:
                json_data.write(line)

    # delete html
    os.system('rm all')

    # read new json data
    geojson_data = open(filepath_json, 'r').read() 
    data = json.loads(geojson_data)

    # iterate through each camera
    for camera in data:

        # default values
        name = ''
        link = ''
        latitude = ''
        longitude = ''

        # iterate through each camera item
        for key, value in camera.items():

            # get link and name
            if key == 'properties':
                title = value.get('title')
                name = title[(title.index('\'>') + 2):title.index('</a>')]
                link = title[title.index('http'):title.index('all')] + 'all'

            # get coordinates
            if key == 'geometry':
                coordinates = value.get('coordinates')
                latitude = coordinates[0]
                longitude = coordinates[1]
            
        # display values
        print(name)
        print(link)
        print(latitude)
        print(longitude)
        print()

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
                    <coordinates>{latitude},{longitude},0</coordinates>
                </Point>
            </Placemark>
        '''

        # add placemark to output file
        output += placemark

    # write output to kml
    with open(filepath_kml, 'w') as kml:
        kml.write(kml_start + output + kml_end)