from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os.path


# Degining app
app = Flask(__name__)
app.secret_key = "suidhfliasdfoagdrgdeocf"


# Initial Page
@app.route('/')
def home():
    return render_template('login.html')


# Your URL page
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
