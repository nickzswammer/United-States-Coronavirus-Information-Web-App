import json
import requests
from flask import render_template, Blueprint
from flask import Flask, redirect, url_for, request
from dotenv import load_dotenv
import os
import mysql.connector
from flaskext.mysql import MySQL
import finnhub

# Create App
app = Flask(__name__)


# Environment Variable API_KEY
load_dotenv()
API_KEY = os.getenv('API_KEY')

# FinnHub
finnhub_client = finnhub.Client(api_key=API_KEY)

# Routes


@app.route('/')
def home():
    data = finnhub_client.covid19()
    data_length = len(data)

    return render_template('index.html', data=data)


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        return render_template('contact.html', success_message=f"Unfortunately, the database hosting this information has expired. Please contact me at zhang.nicholas136@gmail.com")

    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
