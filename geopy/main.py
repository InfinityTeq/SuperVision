#!/usr/bin/env python
# geopy shit
# created by : C0SM0

# imports
import os
import geopy
import folium
import webbrowser

# 40.7484405,-73.9878531 empirte state
# pyscript links
# <link rel="stylesheet" href="https://pyscript.net/alpha/pyscript.css" />
# <script defer src="https://pyscript.net/alpha/pyscript.js"></script>

# map = folium.Map(location=[45.5236, -122.6750])
map = folium.Map(location=[45.372, -121.6972], zoom_start=12, tiles="Stamen Terrain")

tooltip = "Camera"

folium.Marker(
    [45.3288, -121.6625], popup='<a href="https://cosmodiumcs.com">Website</a>', tooltip=tooltip
).add_to(map)
folium.Marker(
    [45.3311, -121.7113], popup="<b>Timberline Lodge</b>", tooltip=tooltip
).add_to(map)


# save and display the map
map.save('index.html')
webbrowser.open('index.html')




