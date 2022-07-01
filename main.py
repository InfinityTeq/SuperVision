#!/usr/bin/env python
# Watchdogs Website
# created by : C0SM0

# imports
import os
import folium # pip req
import urllib.request
from livereload import Server # pip req
from folium.plugins import *
from bs4 import BeautifulSoup # pip req
from flask import Flask, render_template # pip req

import atexit
from apscheduler.schedulers.background import BackgroundScheduler # pip req

# get bus data
def get_bus_data():

    output_list = []

    # get and read bus data
    u = urllib.request.urlopen('http://ctabustracker.com/bustime/map/getBusesForRoute.jsp?route=22')
    data = u.read()

    # parse bus data
    soup = BeautifulSoup(data, "xml")
    bus = soup.find_all('bus')

    # iterate bus data
    for item in bus:

        bus_values = []

        # assign values
        name = item.find('id').text
        longitude = item.find('lon').text
        latitude = item.find('lat').text

        # add values
        bus_values.append(name)
        bus_values.append(longitude)
        bus_values.append(latitude)
        output_list.append(bus_values)

    return output_list

# gets kml data
def get_kml_data(file):

    output_list = []

    # read data
    page = open(file, 'r').read()
    soup = BeautifulSoup(page, "xml")

    # iterate over kml
    placemark = soup.find_all('Placemark')
    for item in placemark:

        camera = []

        # get values
        name = item.find('name').text # name
        link = item.find('value').text # link

        # get and format coordinates
        coordinates = item.find('coordinates').text # coordinates
        coordinates = coordinates.replace("'", '').replace("(",'').replace(")", '')

        # get longitude and latitude
        coordinates = coordinates.split(',')
        longitude = coordinates[0]
        latitude = coordinates[1]

        # add to list
        camera.append(name)
        camera.append(link)
        camera.append(longitude)
        camera.append(latitude)
        output_list.append(camera)

    # returns list of camera data
    return output_list

# main code, makes map
def main():

    kml_directory = 'kml'

    # generate map
    map = folium.Map(zoom_start=12, control_scale=True, width='100%', height='80%')

    # feature group
    fg = folium.FeatureGroup().add_to(map)
    map.add_child(fg)
 
    # plugins
    minimap = MiniMap()
    map.add_child(minimap) # mini map
    LocateControl(auto_start=True).add_to(map) # user location
    Fullscreen().add_to(map) # full screen
    MousePosition().add_to(map) # mouse position coordinates
    folium.features.ClickForMarker().add_to(map) # click for marker
    Geocoder().add_to(map) # search bar
    FloatImage(image='https://static.wixstatic.com/media/1a48ab_c140d7ec1edc4c44aeb9bca9ce00cc3e~mv2.png/v1/fill/w_50,h_50,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/1a48ab_c140d7ec1edc4c44aeb9bca9ce00cc3e~mv2.png', bottom=23, left=0).add_to(map) # floating logo

    # themes
    folium.TileLayer('cartodbdark_matter').add_to(map)
    folium.TileLayer('cartodbpositron').add_to(map)
    folium.TileLayer('stamentoner').add_to(map)
    folium.LayerControl().add_to(map)

    # iterate through kml files
    for kml in os.listdir(kml_directory):
        kml_path = os.path.join(kml_directory, kml)

        print(kml_path)

        # get kml data
        kml_data = get_kml_data(kml_path)
        kml_name = kml[:-4].title()

        # sub_group = FeatureGroupSubGroup(fg, kml_name)
        # map.add_child(sub_group)

        marker_cluster = MarkerCluster(name=kml_name)
        marker_cluster.add_to(fg)
        # sub_group.add_child(marker_cluster)

        # iterate over and assign kml data
        for data in kml_data:

            # get values from kml data
            name = data[0]
            link = data[1]
            longitude = data[2]
            latitude = data[3]

            # add marker to map
            folium.Marker([latitude, longitude], popup='<a href={LINK} target="_blank">View Camera</a>'.format(LINK=link), tooltip=name, icon=folium.Icon(color="black", icon="camera")).add_to(marker_cluster)

    # iterate through bust data
    buses = get_bus_data()

    # iterate through buses
    for bus in buses:

        # get values from bus data
        name = bus[0]
        longitude = bus[1]
        latitude = bus[2]

        # create marker
        folium.Marker([latitude, longitude], popup='Bus'.format(LINK=link), tooltip=name, icon=folium.Icon(color="green", icon="car")).add_to(marker_cluster)

    # save and display the map
    map.save('templates/index.html')

    # add realtime visualization to html
    realtime = '''
    L.control.liveupdate ({
            update_map: function () {
            },
            position: 'topleft',
            interval: 5000
    })
    .addTo(map)
    .startUpdating();
    </script>
    '''
    read_index = open('templates/index.html', 'r').readlines()
    map_name = ''
    with open('templates/index.html', 'w') as index:
        for line in range(len(read_index) - 1):
            # # var map_51e7d4c78adf02fa68853a29191878a2 = L.map(
            # if read_index[line].strip().endswith('L.map('):
            #     map_name = read_index[line].strip(' ').replace('\t', '').replace('var ','').replace(' = L.map(','')
            #     print(map_name)
            #     print()

            index.write(read_index[line])
        index.write(realtime)

    # return map._repr_html_()

# flask processes
app = Flask(__name__)

@app.route("/")

def index():
    main()

    # imported code
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=main, trigger="interval", seconds=5)
    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

    return render_template('index.html')
    # return main()

if __name__ == "__main__":
    # server = Server(app.wsgi_app)
    # server.serve()
    app.run(debug=True)





