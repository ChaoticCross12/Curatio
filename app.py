from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os.path
import ipinfo

# google maps
from flask_googlemaps import GoogleMaps, Map
from googleplaces import GooglePlaces, types, lang

# Begining app
app = Flask(__name__)
app.secret_key = "suidhfliasdfoagdrgdeocf"
app.run(debug=True)

MAPS_API_KEY = 'AIzaSyCskEcqqtB89CfG-jJXihqF20SZSlRxzFo'
app.config['GOOGLEMAPS_KEY'] = MAPS_API_KEY
GoogleMaps(app)


# Initial Page
@app.route('/')
def home():
    return render_template('login.html')


# Sign Up page
@app.route('/signUp', methods = ['GET', 'POST'])
def signUpPage():
    return render_template('signUp.html')




# Logging in
@app.route('/placeholder', methods = ['GET', 'POST'])
def your_url():

    # Check method
    if request.method == 'POST':

        # Dictioary for data
        loginData = {}

        # Checking if json file exists
        if os.path.exists('loginInfo.json'):

            # Opening json file
            with open('loginInfo.json') as login_file:

                # Adding data from json file to dictionary
                loginData = json.load(login_file)

        # Checking if key in dictionary
        if request.form['username'] in loginData[request.form['client']].keys():
            if request.form['password'] == loginData[request.form['client']][request.form['username']]:

                # If correct username and password
                return render_template('placeholder.html')


@app.route('/services')
def services():
    # list names of services (shown to user)
    services = [
               "Treatment",
               "Find nearest clinic",
               "Find nearest drugstore"
               ]
    # links of services
    services_link = [
                    "treatment",
                    "nearest_clinic",
                    "nearest_drugstore"
                    ]


    return render_template('services.html', services=services,
                            services_link=services_link)


@app.route('/nearest_clinic')
def clinic():
    # calls mapview() and displays "hospital"
    items = mapview("hospital")
    return render_template('nearest_clinic.html', map=items[0], name=items[1])


@app.route('/nearest_drugstore')
def drugstore():
    # calls mapview() and displays "pharmacy"
    items = mapview("pharmacy")
    return render_template('nearest_drugstore.html', map=items[0], name=items[1])


# detect location using IP
def ip_coordinates():
    ipinfo_token = '0562b9f1a0bc99'
    handler = ipinfo.getHandler(ipinfo_token)
    ip_data = handler.getDetails()
    # city = data.city + data.region + data.country
    latitude = ip_data.latitude
    longitude = ip_data.longitude
    return latitude, longitude


def mapview(itemtype):
    if itemtype == "hospital":
        search_type = [types.TYPE_HOSPITAL]
        pass
    if itemtype == "pharmacy":
        search_type = [types.TYPE_PHARMACY]
        pass
    
    places = GooglePlaces(MAPS_API_KEY)
    coordinates = ip_coordinates()
    latitude = coordinates[0]
    longitude = coordinates[1]

    search_result = places.nearby_search(
        lat_lng={'lat': latitude, 'lng': longitude},
        radius=3000,
        types=search_type
    )

    if search_result.has_attributions:
        print(search_result.html_attributions)

    markers = []
    name = []
    for place in search_result.places:
        # place.get_details()
        item_name = place.name
        item_latitude = place.geo_location['lat']
        item_longitude = place.geo_location['lng']
        # item_address = place.formatted_address
        location_of_item = { 'lat': str(item_latitude), 'lng': str(item_longitude), 'infobox': item_name}
        markers.append(location_of_item)
        name.append(item_name)

    map_data = Map(
        identifier="map",
        lat=item_latitude,
        lng=item_longitude,
        markers=markers,
        style="height:80%;width:100%;margin:auto;",
        zoom=16
    )

    return map_data, name
