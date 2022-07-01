from bs4 import BeautifulSoup # pip req

# gets kml data
def get(file):

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