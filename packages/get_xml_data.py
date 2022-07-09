import urllib.request
from bs4 import BeautifulSoup # pip req
from opensky_api import OpenSkyApi

key = open('../creds.key', 'r').read()
api = OpenSkyApi(username='CosmodiumCS', password=key)
planes = api.get_states()

def get_flights(save_file_name):
   
    # values
    # account for ouptut
    count = 0
    output = ''

    # iterate through each camera
    for plane in planes.states:

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
    <planes>
    '''

    kml_end = '''
    </planes>
    '''

    final_text = (kml_start + output + kml_end)

    with open(f'xml/{save_file_name}', 'w') as xml:
        xml.write(final_text)

    return final_text

# get xml data
def get(url, save_file_name):

    # data = ''

    # get and read xml data
    if 'http' in url:
        u = urllib.request.urlopen(url)
        data = u.read()

        # save data
        with open(f'xml/{save_file_name}', 'wb') as xml:
            xml.write(data)

        # return xml data
        return data.decode('utf-8').replace('\n','')
    
    # else:
    return get_flights(save_file_name)
