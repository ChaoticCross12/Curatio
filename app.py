from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os.path
import ipinfo
from square.client import Client
import json



# square API
client = Client(
    access_token='SQUARE_API_KEY',
    environment='production',)

customers_api = client.customers

# google maps
from flask_googlemaps import GoogleMaps, Map
from googleplaces import GooglePlaces, types, lang

# Begining app
app = Flask(__name__)
app.secret_key = "suidhfliasdfoagdrgdeocf"
#app.run(debug=True)

MAPS_API_KEY = 'GOOGLE_MAPS_API_KEY'
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


# Doctor Sign Up page
@app.route('/docSignUp', methods = ['GET', 'POST'])
def docSignUpPage():
    return render_template('docSignUp.html')


# Logging in
@app.route('/home', methods = ['GE9T', 'POST'])
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

                # returns homepage
                return services()

            else:
                flash('Incorrect username or password')
                return render_template('login.html')


        else:
            flash('Incorrect username or password')
            return render_template('login.html')


#### HOME PAGE ####

@app.route('/services')
def services():
    # list names of services (shown to user)
    services = [
               "Treatment Physical",
               "Treatment mental",
               "Find nearest clinic",
               "Find nearest drugstore"
               ]
    # routes of services
    services_link = [
                    "treatment_physical",
                    "treatment_mental",
                    "nearest_clinic",
                    "nearest_drugstore"
                    ]

    return render_template('services.html', services=services,
                            services_link=services_link)



@app.route('/treatment_physical')
def treatment_physical():
    symptoms = """Eye Irritation
        Runny nose
        Stuffy nose
        Puffy/Watery eyes
        Inflamed/Itchy nose and throat
        Skin rash
        Wheezing
        Gastrointestinal distress
        Lightheadedness/Fainting
        Fever
        Headache
        Dry cough
        Fatigue
        Burning sensation
        Watery, loose stools
        Frequent bowel movements
        Cramping or pain in the abdomen
        Nausea
        Insomnia
        Vomiting
        Hepatitis"""
    symptoms = symptoms.replace("\t","").split("\n")
    return render_template('treatment_physical.html', symptoms=symptoms)


@app.route('/treatment_mental')
def treatment_mental():

    return render_template('treatment_mental.html')


@app.route('/nearest_clinic')
def clinic():
    # displays "hospital" in map
    items = mapview("hospital")
    return render_template('map.html', title="Clinic", map=items[0], name=items[1], maps_link=items[2])


@app.route('/nearest_drugstore')
def drugstore():
    # displays "pharmacy" in map
    items = mapview("pharmacy")
    return render_template('map.html', title="Drugstore", map=items[0], name=items[1], maps_link=items[2])


# detect location using IP
def ip_coordinates():
    ipinfo_token = '0562b9f1a0bc99'
    ip_data = ipinfo.getHandler(ipinfo_token).getDetails()
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
    if itemtype == "":
        return "itemtype not provided"

    # using googleplaces to search nearby
    places = GooglePlaces(MAPS_API_KEY)
    coordinates = ip_coordinates()
    latitude = coordinates[0]
    longitude = coordinates[1]

    search_result = places.nearby_search(
        lat_lng={'lat': latitude, 'lng': longitude},
        radius=2000,
        types=search_type
    )

    if search_result.has_attributions:
        print(search_result.html_attributions)

    markers = []
    name = []
    maps_link = []

    for place in search_result.places:
        # place.get_details()
        item_name = place.name
        item_latitude = place.geo_location['lat']
        item_longitude = place.geo_location['lng']
        # item_address = place.formatted_address
        location_of_item = { 'lat': str(item_latitude), 'lng': str(item_longitude), 'infobox': "<a id='pointerlink' href='https://www.google.com/maps/search/?api=1&query=" + item_name.replace(" ", "+") + "'>" + item_name + "</a>"}
        markers.append(location_of_item)
        name.append(item_name)
        #maps_link.append("http://maps.google.com/?q=" + str(item_latitude) + "," + str(item_longitude))
        maps_link.append("https://www.google.com/maps/search/?api=1&query=" + item_name.replace(" ", "+"))


    # using flask_googlemaps to display map
    map_data = Map(
        identifier="map",
        lat=item_latitude,
        lng=item_longitude,
        markers=markers,
        style="height:95%;width:70%;margin:0px;",
        zoom=16
    )

    return map_data, name, maps_link


# Signing up new user
@app.route('/', methods = ['GET', 'POST'])
def storeUserInfo():
    # Check method
    if request.method == 'POST':

        # Dictioary for data
        OldLoginData = {}

        # Checking if json file exists
        if os.path.exists('loginInfo.json'):

            with open('loginInfo.json') as old_login_file:

                # Adding data from json file to dictionary
                OldLoginData = json.load(old_login_file)
                loginDataSet = OldLoginData[request.form['client']]

                if request.form['username'] in loginDataSet.keys():
                    flash('Username already taken')
                    return render_template('signUp.html')
                    # FLASK MESSAGE

                else:
                    # NEEDS WORK
                    loginDataSet[request.form['username']]  = request.form['password']
                    OldLoginData[request.form['client']] = loginDataSet
                    #

            with open('loginInfo.json', 'w') as old_login_file:

                # Adding dictionary to json file
                json.dump(OldLoginData, old_login_file)
                return render_template('login.html')



# Contact a general practitioner
@app.route('/consult')
def consult():

        # Needs to redirect to the port where the video module is running
        return redirect('http://localhost:3000')

# Search results
@app.route('/search', methods = ['GET', 'POST'])
def list():
    try:
        x = list_all_customers()["customers"]
    except KeyError:
        return "no registered users found"

    x = list_all_customers()["customers"]
    ids = []
    names = []
    notes = []
    phones = []
    for item in x:
        print(item)
        ids.append(item["id"])
        names.append(item["nickname"])
        notes.append(item["note"])
        phones.append(item["phone_number"])

    total = len(ids)
    return render_template('list.html', names=names, ids=ids, notes=notes, phones=phones, total=total)


# Doctor sign up
@app.route('/docSigned', methods = ['GET', 'POST'])
def docSignUpFunc():
    # Check method
    if request.method == 'POST':

        # Dictioary for data
        OldLoginData = {}

        # Checking if json file exists
        if os.path.exists('loginInfo.json'):

            with open('loginInfo.json') as old_login_file:

                # Adding data from json file to dictionary
                OldLoginData = json.load(old_login_file)
                loginDataSet = OldLoginData[request.form['client']]

                if request.form['username'] in loginDataSet.keys():
                    flash('Username already taken')
                    return render_template('signUp.html')
                    # FLASK MESSAGE

                else:
                    # NEEDS WORK
                    loginDataSet[request.form['username']]  = request.form['password']
                    OldLoginData[request.form['client']] = loginDataSet
                    #

            with open('loginInfo.json', 'w') as old_login_file:

                # Adding dictionary to json file
                json.dump(OldLoginData, old_login_file)

                # sign up successful
                name = request.form['name']
                email = request.form['email']
                phone = request.form['phonenumber']
                address = request.form['address']
                note = request.form['note']

                # writing new doctor details
                new_customer(name, email, phone, address, note)

                return render_template('login.html')

    return redirect('/')



def new_customer(name, email, phone, address, note):
    body = {}
    body['nickname'] = name
    body['email_address'] = email
    body['phone_number'] = phone
    body['address'] = {}
    body['address']['add'] = address
    body['note'] = note
    print(body)
    result = customers_api.create_customer(body)
    if result.is_success():
        return result.body
    elif result.is_error():
        return result.errors
    else:
        return "unknown error"


def list_all_customers():

    result = customers_api.list_customers()

    if result.is_success():
        return result.body

    elif result.is_error():
        return result.errors
    else:
        return "unknown error"


def delete_customer(id):

    result = customers_api.delete_customer(id)

    if result.is_success():
        return result.body
    elif result.is_error():
        return result.errors
