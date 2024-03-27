import os.path

import numpy as np
import requests


def get_epc_label(consumption):
    if consumption == 0:
        return "A+", os.path.join('images', 'aplus.png')
    elif consumption <= 100:
        return "A", os.path.join('images', 'a.png')
    elif consumption <= 200:
        return "B", os.path.join('images', 'b.png')
    elif consumption <= 300:
        return "C", os.path.join('images', 'c.png')
    elif consumption <= 400:
        return "D", os.path.join('images', 'd.png')
    elif consumption <= 500:
        return "E", os.path.join('images', 'e.png')
    elif consumption <= 600:
        return "F", os.path.join('images', 'f.png')
    else:
        return "G", os.path.join('images', 'g.png')


def get_coordinates(number, street, postalcode):
    """
    Get the latitude and longitude coordinates of an address using OpenStreetMap Nominatim API, by address
    """
    root_url = "https://nominatim.openstreetmap.org/search?"
    number = f"{number}" if number else ""
    street = f"{street}" if street else ""
    postalcode = f"{postalcode}" if postalcode else ""

    params = {"street": f"{street} {number}",
              "country": "belgium",
              "postalcode": postalcode,
              "format": "jsonv2",
              "addressdetails": "1"}
    response = requests.get(root_url, params=params)
    data = response.json()
    if not data:
        print(f'adress not found: {postalcode}, {street}, {number}')
        return 0, 0

    print(f'adress found: {postalcode}, {street}, {number}')
    lat = float(data[0]["lat"])
    lon = float(data[0]["lon"])
    return lat, lon
