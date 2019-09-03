#!/usr/bin/env python3
import os
import os.path
import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from flask import Flask, jsonify, render_template, Response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://gfsxlvmtqwnogp:534030f82dc0d74634d2253fa43f403ecbd9dd50346f7c140a3564d03c2a2506@ec2-184-73-169-163.compute-1.amazonaws.com:5432/d806adirak8md8"
db = SQLAlchemy(app)
engine = db.create_engine('postgres://gfsxlvmtqwnogp:534030f82dc0d74634d2253fa43f403ecbd9dd50346f7c140a3564d03c2a2506@ec2-184-73-169-163.compute-1.amazonaws.com:5432/d806adirak8md8', encoding='latin1', echo=True)
connection = engine.connect()
metadata = db.MetaData()
trips_raw = db.Table('trips_raw', metadata, autoload=True, autoload_with=engine)
query = db.select([trips_raw])
ResultProxy = connection.execute(query)
ResultSet = ResultProxy.fetchall()
df = pd.read_sql(query, engine)
# print(df)
# reflect an existing database into a new model
#Base = automap_base()
# reflect the tables
#Base.prepare(db.engine, reflect=True)

# Save references to each table
#Samples_Metadata = Base.classes.sample_metadata
# Trips_raw = Base.classes.trips_raw
# stmt = db.session.query(Trips_raw).statement
# df = pd.read_sql_query(stmt, db.session.bind)
# print(df)

def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))

def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)
        # Figure out how flask returns static files
        # Tried:
        # - render_template
        # - send_file
        # This should not be so non-obvious
        return open(src).read()
    except IOError as exc:
        return str(exc)


@app.route('/', methods=['GET'])
def index():  # pragma: no cover
    content = get_file('usage.html')
    return Response(content, mimetype="text/html")


@app.route("/trips_raw")
def names():
    resp = Response(response=df.to_json(),
        status=200,
        mimetype="application/json")
    return(resp)


@app.route("/metadata/<sample>")
def sample_metadata(sample):
    """Return the MetaData for a given sample."""
    sel = [
        Samples_Metadata.trip_duration,
        Samples_Metadata.start_time,
        Samples_Metadata.stop_time,
        Samples_Metadata.start_station_id,
        Samples_Metadata.start_station_name,
        Samples_Metadata.end_station_name,
        Samples_Metadata.bike_id,
    ]

    results = db.session.query(*sel).filter(Samples_Metadata.sample == sample).all()

    # Create a dictionary entry for each row of metadata information
    sample_metadata = {}
    for result in results:
        sample_metadata["sample"] = result[0]
        sample_metadata["Trip Duration"] = result[1]
        sample_metadata["Start Time"] = result[2]
        sample_metadata["Stop Time"] = result[3]
        sample_metadata["Start Station id"] = result[4]
        sample_metadata["Start Station Name"] = result[5]
        sample_metadata["End Station Name"] = result[6]

    print(sample_metadata)
    return jsonify(sample_metadata)


@app.route("/samples/<sample>")
def samples(sample):
    """Return `otu_ids`, `otu_labels`,and `sample_values`."""
    stmt = db.session.query(Samples).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Filter the data based on the sample number and
    # only keep rows with values above 1
    sample_data = df.loc[df[sample] > 1, ["otu_id", "otu_label", sample]]

    # Sort by sample
    sample_data.sort_values(by=sample, ascending=False, inplace=True)

    # Format the data to send as json
    data = {
        "otu_ids": sample_data.otu_id.values.tolist(),
        "sample_values": sample_data[sample].values.tolist(),
        "otu_labels": sample_data.otu_label.tolist(),
    }
    return jsonify(data)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def get_resource(path):  # pragma: no cover
    mimetypes = {
        ".css": "text/css",
        ".html": "text/html",
        ".js": "application/javascript",
    }
    complete_path = os.path.join(root_dir(), path)
    ext = os.path.splitext(path)[1]
    mimetype = mimetypes.get(ext, "text/html")
    content = get_file(complete_path)
    return Response(content, mimetype=mimetype)

if __name__ == "__main__":
    app.run()