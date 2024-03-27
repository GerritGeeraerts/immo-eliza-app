import pickle

import numpy as np
import requests


def load_model_from_pickle(path: str):
    with open(path, 'rb') as file:
        model = pickle.load(file)
        return model

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
        return np.nan, np.nan

    print(f'adress found: {postalcode}, {street}, {number}')
    lat = float(data[0]["lat"])
    lon = float(data[0]["lon"])
    return lat, lon
