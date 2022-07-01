#!/usr/bin/env python
# SuperVision
# created by : C0SM0

# imports
import os
import folium # pip req
from folium.plugins import *
from flask import Flask, render_template, send_from_directory # pip req
from flask_navigation import Navigation

# packages
from packages import get_bus_data
from packages import get_real_time
from packages import get_kml_data

# main code, makes map
def main():

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
    kml_directory = 'kml'
    for kml in os.listdir(kml_directory):

        kml_path = os.path.join(kml_directory, kml)
        print(kml_path)

        # get kml data
        kml_data = get_kml_data.get(kml_path)
        kml_name = kml[:-4].title()

        # marker clusters
        marker_cluster = MarkerCluster(name=kml_name)
        marker_cluster.add_to(fg)

        # iterate over and assign kml data
        for data in kml_data:

            # get values from kml data
            name = data[0]
            link = data[1]
            longitude = data[2]
            latitude = data[3]

            # add marker to map
            folium.Marker([latitude, longitude], popup='<a href={LINK} target="_blank">View Camera</a>'.format(LINK=link), tooltip=name, icon=folium.Icon(color="black", icon="camera")).add_to(marker_cluster)

    # save and display the map
    map.save('templates/index.html')
    # return map._repr_html_()

# flask processes
app = Flask(__name__)

# render home page
# NOTE: "get_bus_data" is referenced twice
@app.route("/")
def index():
    main()
    get_real_time.get()
    get_bus_data.get()

    return render_template('index.html')
    # return main()

# TODO: loop this and iterate through all xml
@app.route("/xml/bus.xml")
def bus_xml():
    return get_bus_data.get()

if __name__ == "__main__":
    app.run(debug=True)
