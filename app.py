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
PASS = os.getenv('PASSWORD')
API_KEY = os.getenv('API_KEY')

# FinnHub
finnhub_client = finnhub.Client(api_key=API_KEY)

# Connect with MySQL Database
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'sql3415644'
app.config['MYSQL_DATABASE_PASSWORD'] = PASS
app.config['MYSQL_DATABASE_DB'] = 'sql3415644'
app.config['MYSQL_DATABASE_HOST'] = 'sql3.freemysqlhosting.net'
mysql.init_app(app)

connection = mysql.connect()
cursor = connection.cursor()


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

        insertdatabase = 'INSERT INTO users (name, email, message) VALUES (%s, %s, %s)'
        inputs = (name, email, message)

        cursor.execute(insertdatabase, inputs)
        connection.commit()

        return render_template('contact.html', success_message="Message sent successfully. I will reach out to you shortly.")

    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
