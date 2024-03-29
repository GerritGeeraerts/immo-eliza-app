import json
import os.path

import streamlit as st
import requests
from streamlit.logger import get_logger

from config import POSTAL_CODES
from utils import get_epc_label, get_coordinates

logger = get_logger(__name__)

# logger.debug(json.dumps(dict(st.session_state)))
if 'address_expander_expanded' not in st.session_state:
    st.session_state.address_expander_expanded = True

subtype_options = {
    '🏠 House': 'HOUSE',
    '🏢 Apartment': 'APARTMENT',
    '🏡 Villa': 'VILLA',
    'Mansion': 'MANSION',
    'Exceptional Property': 'EXCEPTIONAL_PROPERTY',
    'Penthouse': 'PENTHOUSE',
    'Duplex': 'DUPLEX',
    'Ground Floor': 'GROUND_FLOOR',
    'Town House': 'TOWN_HOUSE',
    'Flat Studio': 'FLAT_STUDIO',
    'Service Flat': 'SERVICE_FLAT',
}
state_of_building_options = {
    'New': 'NEW',
    'Just Renovated': 'JUST_RENOVATED',
    'Good': 'GOOD',
    'To Be Done Up': 'TO_BE_DONE_UP',
    'To Renovate': 'TO_RENOVATE',
}
kitchen_options = {
    'Hyper Equipped': 'HYPER_EQUIPPED',
    'Equipped': 'EQUIPPED',
    'Semi Equipped': 'SEMI_EQUIPPED',
    'Not Equipped': 'NOT_EQUIPPED',
}
postal_codes = {'': None}
postal_codes.update(POSTAL_CODES)


def predict_price(data):
    backend_url = os.getenv('BACKEND_URL')
    base_url = backend_url if backend_url else 'http://0.0.0.0:8000'
    url = f"{base_url}/property-value-inference/"
    logger.info(f"Sending request to {url} with data: {data}")
    response = requests.post(url, json=data)
    if response.status_code == 200:
        logger.info(f"Response: {response.json()}")
        return response.json()
    else:
        st.error("Failed to get the prediction. Please check the API and try again.")
        return None


def recalculate_prediction():
    data = {
        "Habitable Surface": st.session_state.get("Habitable Surface", 100),
        "Subtype": subtype_options[st.session_state.get("Subtype", '🏠 House')],
        "Land Surface": st.session_state.get("Land Surface", 500),
        "Bedroom Count": st.session_state.get("Bedroom Count", 3),
        "Bathroom Count": st.session_state.get("Bathroom Count", 3),
        "Toilet Count": st.session_state.get("Toilet Count", 3),
        "Facades": st.session_state.get("Facades", 4),
        "Consumption": st.session_state.get("Consumption", 100),
        "Kitchen Type": kitchen_options[st.session_state.get("Kitchen Type", 'Equipped')],
        "State of Building": state_of_building_options[st.session_state.get("State of Building", 'New')],
        "Postal Code": POSTAL_CODES[st.session_state.get("Postal Code", "1000 - Brussel")],
        "Latitude": st.session_state.get("Latitude") if st.session_state.get("Latitude") else None,
        "Longitude": st.session_state.get("Longitude") if st.session_state.get("Longitude") else None,
    }
    logger.info(json.dumps(data))
    prediction = predict_price(data)
    if prediction:
        st.session_state['price'] = price = prediction.get('value')
        st.session_state['unit'] = unit = prediction.get('unit')
        output = f"The predicted price of the house is:\n# {unit} {f'{price:,.0f}'.replace(',', '.')},-"
        logger.info(output)
        st.session_state['output'] = output


def get_coordinates_for_adress():
    lat, lon = get_coordinates(
        st.session_state['Street Number'],
        st.session_state.get("Street Name"),
        POSTAL_CODES[st.session_state.get("Postal Code", "1000 - Brussel")]
    )
    st.session_state['Latitude'] = lat
    st.session_state['Longitude'] = lon
    if lat == 0 or lon == 0:
        logger.info(f"Address not found: {st.session_state.get('Postal Code')}, {st.session_state.get('Street Name')}, "
                    f"{st.session_state['Street Number']}")
        st.session_state["address_found"] = False
        st.session_state["load_address_success"] = False
        setattr(st.session_state, 'address_expander_expanded', True)
        return
    logger.info(f"Address found: {st.session_state.get('Postal Code')}, {st.session_state.get('Street Name')}, "
                f"{st.session_state['Street Number']}, Latitude: {lat}, Longitude: {lon}")
    st.session_state["address_found"] = True
    st.session_state["load_address_success"] = True
    setattr(st.session_state, 'address_expander_expanded', False)
    recalculate_prediction()


# Base Layout
prediction_msg = 'Enter an address and change features to get a prediction'
if 'output' in st.session_state:
    prediction_msg = f"{st.session_state['output']}"
title = st.sidebar.title('Prediction')
st.sidebar.success(prediction_msg)
st.image(os.path.join('images', 'house.png'), use_column_width='always')
st.title('🇧🇪 Belgian House Price Prediction')

# Address
st.subheader('Address')
with st.expander("Edit Address", expanded=st.session_state.address_expander_expanded):
    st.session_state['load_address_disabled'] = False
    st.selectbox(
        'Postal Code', key="Postal Code",
        options=postal_codes,
        index=0,
    )

    # Postal Code
    if not st.session_state.get("Postal Code"):
        st.error('Please select a postal code')
        st.session_state['load_address_disabled'] = True

    # Street Name
    st.text_input('Street Name', key="Street Name", )
    if not st.session_state.get("Street Name"):
        st.error('Please enter a street name')
        st.session_state['load_address_disabled'] = True

    # Street Number
    st.number_input(
        'Street Number (No letters)]', key="Street Number",
        step=1,
        format="%d"
    )
    if not st.session_state.get('Street Number'):
        st.error('Please enter a street number')
        st.session_state['load_address_disabled'] = True

    # Address Not Found Error
    if not st.session_state.get("address_found", True):
        st.error('Address not found. Please check the address details and try again, '
                 'You can also try adding a nearby address')
        st.session_state['load_address_disabled'] = False

    # Load Address Button
    st.button('Load Address',
              on_click=get_coordinates_for_adress, disabled=st.session_state['load_address_disabled'])

# Address Loaded Success
if st.session_state.get('load_address_success', False):
    st.success(
        f"Address Loaded: **{st.session_state['Street Name']} {st.session_state['Street Number']}, "
        f"{POSTAL_CODES.get(st.session_state['Postal Code'])}** "
        f"[Longitude: {str(st.session_state.get('Longitude'))[:6]}, "
        f"Latitude: {str(st.session_state.get('Latitude'))[:6]}]")

# Feature selection
if st.session_state.get('load_address_success', False):
    # Housing type
    st.subheader('Housing Type')
    st.selectbox(
        'Subtype', key='Subtype',
        options=subtype_options,
        index=0,
        on_change=recalculate_prediction
    )

    # Number of Facades
    st.slider(
        'Facades', key="Facades",
        min_value=2, max_value=4, value=4, step=1,
        on_change=recalculate_prediction
    )

    # Surface
    st.subheader('Surface')
    st.slider(
        'Habitable Surface', key="Habitable Surface",
        min_value=20, max_value=1000, value=100, step=5, format="%d m²",
        on_change=recalculate_prediction
    )

    # Land Surface
    if subtype_options[
        st.session_state.get('Subtype')] != 'APARTMENT':  # Check if the selected subtype is not 'APARTMENT'
        land_surface = st.slider(
            'Land Surface', key="Land Surface",
            min_value=0, max_value=10000, value=500, step=25, format="%d m²",
            on_change=recalculate_prediction,
        )
    else:
        st.session_state['Land Surface'] = 0  # For apartments, land surface is 0

    st.subheader('Rooms')
    # Bedroom Count
    bedroom_count = st.slider(
        'Bedroom Count', key="Bedroom Count",
        min_value=0, max_value=10, value=3, step=1,
        on_change=recalculate_prediction,
    )

    # Bathroom Count
    bathroom_count = st.slider(
        'Bathroom Count', key="Bathroom Count",
        min_value=0, max_value=10, value=1, step=1,
        on_change=recalculate_prediction,
    )

    # Toilet Count
    toilet_count = st.slider(
        'Toilet Count', key="Toilet Count",
        min_value=0, max_value=10, value=2, step=1,
        on_change=recalculate_prediction,
    )

    st.subheader('State of the House')
    # State of Building
    state_of_building = st.selectbox(
        'State of Building', key="State of Building",
        options=state_of_building_options, index=1,
        on_change=recalculate_prediction,
    )

    # Kitchen Type
    kitchen_type = st.selectbox(
        'Kitchen Type', key="Kitchen Type",
        options=kitchen_options, index=1,
        on_change=recalculate_prediction,
    )

    # Energy Consumption
    consumption = st.slider(
        'Consumption', key="Consumption",
        min_value=0, max_value=1000, value=100, step=10, format="%d kWh/m²/year",
        on_change=recalculate_prediction
    )
    epc_category, epc_image_path = get_epc_label(consumption)
    st.image(epc_image_path, width=100)

st.success(prediction_msg)
st.text(
    "The model is predicting listing price as it is trained on listing prices.\n"
    "The model is trained on Belgian real estate data.\n"
    "It is trained on a limited set of features that are listed above.\n"
)
