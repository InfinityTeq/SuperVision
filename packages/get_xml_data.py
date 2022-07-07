import urllib.request
from bs4 import BeautifulSoup # pip req

# get xml data
def get(url, save_file_name):

    # get and read xml data
    u = urllib.request.urlopen(url)
    data = u.read()

    # save data
    with open(f'xml/{save_file_name}', 'wb') as xml:
        xml.write(data)

    # return xml data
    return data.decode('utf-8').replace('\n','')
    