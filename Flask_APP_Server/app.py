import os
# import pandas as pd
# import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
# import json

app = Flask(__name__)
#################################################
# Database Setup
#################################################
# USe sqlalchemy to connect to the PostgreSQL database
# Designate the database URI (for deployment later)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://username:password@localhost:5432/CitiBike_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning
# setup a SQLAlchemy app
db = SQLAlchemy(app)
# reflect an existing database into a new model (many to many relationship )
#Base = automap_base()
# reflect the tables (many to many relationship)
#Base.prepare(db.engine, reflect=True)

class station(db.Model):
    __tablename__ = 'station'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    lat = db.Column(db.String(64))
    long = db.Column(db.String(64))

    def __init__(self, name, lat, long):
        self.name = name
        self.lat = float(lat)
        self.long = float(long)

# create route that renders home.html template
@app.route("/")
def home():
   stations=station.query.all()
   """Return the homepage."""
   return render_template('home.html', myStations=stations)


@app.route("/apidata")
def stationsAPI():
    results=station.query.all()

    name = [result.name for result in results]
    lat = [result.lat for result in results]
    long = [result.long for result in results]

    api_data = [{
        "name": name,
        "lat": lat,
        "long": long,
           
    }]
    return jsonify(api_data)

if __name__ == '__main__':
   app.run()


