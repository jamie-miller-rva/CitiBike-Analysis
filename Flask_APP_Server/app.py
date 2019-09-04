import os
# import pandas as pd
# import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
# import json
app = Flask(__name__)
#################################################
# Database Setup
#################################################
# USe sqlalchemy to connect to the PostgreSQL database
# Designate the database URI (for deployment later)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:postgres@localhost:5432/CitiBike_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning
# setup a SQLAlchemy app
db = SQLAlchemy(app)
# reflect an existing database into a new model (many to many relationship )
#Base = automap_base()
# reflect the tables (many to many relationship)
#Base.prepare(db.engine, reflect=True)
class stations(db.Model):
   __tablename__ = 'stations'
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(64))
   latitude = db.Column(db.String(64))
   longitude = db.Column(db.String(64))
   def __init__(self, name, latitude, longitude):
       self.name = name
       self.latitude = float(latitude)
       self.longitude = float(longitude)
# create route that renders home.html template
@app.route("/")
def home():
  varStations=stations.query.all()
  """Return the homepage."""
  return render_template('home.html', myStations=varStations)
@app.route("/apidata")
def stationsAPI():
   results=stations.query.all()
   name = [result.name for result in results]
   latitude = [result.latitude for result in results]
   longitude = [result.longitude for result in results]
   api_data = [{
       "name": name,
       "latitude": str(latitude),
       "longitude": str(longitude),
   }]
   return jsonify(api_data)
if __name__ == '__main__':
  app.run()