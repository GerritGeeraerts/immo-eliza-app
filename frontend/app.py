from pprint import pprint

import streamlit as st
import requests

# Streamlit app layout
st.title('House Price Prediction')

# Input fields
habitable_surface = st.slider(
    'Habitable Surface',
    min_value=0, max_value=1000, value=100, step=1, format="%d m²"
)
subtype = st.selectbox(
    'Subtype',
    options=['HOUSE', 'VILLA', 'MANSION', 'EXCEPTIONAL_PROPERTY', 'APARTMENT', 'PENTHOUSE', 'DUPLEX', 'GROUND_FLOOR',
             'TOWN_HOUSE', 'FLAT_STUDIO', 'SERVICE_FLAT'],
    index=0
)
land_surface = st.slider(
    'Land Surface',
    min_value=0, max_value=10000, value=500, step=1, format="%d m²"
)
bedroom_count = st.slider(
    'Bedroom Count',
    min_value=0, max_value=10, value=3, step=1
)
bathroom_count = st.slider(
    'Bathroom Count',
    min_value=0, max_value=10, value=1, step=1
)
toilet_count = st.slider(
    'Toilet Count',
    min_value=0, max_value=10, value=2, step=1
)
facades = st.slider(
    'Facades',
    min_value=2, max_value=4, value=4, step=1
)
consumption = st.slider(
    'Consumption',
    min_value=0, max_value=1000, value=100, step=1, format="%d kWh/m²/year"
)
kitchen_type = st.selectbox(
    'Kitchen Type',
    options=['HYPER_EQUIPPED', 'EQUIPPED', 'SEMI_EQUIPPED', 'NOT_EQUIPPED'],
    index=1
)
state_of_building = st.selectbox(
    'State of Building',
    options=['NEW', 'GOOD', 'TO_BE_DONE_UP', 'TO_RENOVATE', 'JUST_RENOVATED'],
    index=0
)
postal_code = st.selectbox(
    'Postal Code',
    options=[1000, 9000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 9451],
    index=0
)

# Button to predict price
if st.button('Predict Price'):
    # API request
    url = 'http://127.0.0.1:8000/property-value-inference/'
    data = {
        "Habitable Surface": habitable_surface,
        "Subtype": subtype,
        "Land Surface": land_surface,
        "Bedroom Count": bedroom_count,
        "Bathroom Count": bathroom_count,
        "Toilet Count": toilet_count,
        "Facades": facades,
        "Consumption": consumption,
        "Kitchen Type": kitchen_type,
        "State of Building": state_of_building,
        "Postal Code": postal_code
    }
    pprint(data)
    response = requests.post(url, json=data)

    if response.status_code == 200:
        price = response.json().get('value')
        unit = response.json().get('unit')
        st.success(f"The predicted price of the house is: {unit} {price}")
    else:
        st.error("Failed to get the prediction. Please check the API and try again.")
