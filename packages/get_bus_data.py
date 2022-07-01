import urllib.request
from bs4 import BeautifulSoup # pip req

# get bus data
def get():

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

    # save data
    with open('xml/bus.xml', 'wb') as xml:
        xml.write(data)

    return data.decode('utf-8').replace('\n','')