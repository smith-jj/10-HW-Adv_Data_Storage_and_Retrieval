import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Passenger = Base.classes.passenger

# Create our session (link) from Python to the DB

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################


@app.route("/")
def Welcome():
    """List all available api routes."""
    return (
        f"Welcome to the Surf's Up API!"
        f"Available Routes:<br/>"
        f"/api/v1.0/surfs-up"
    )


@app.route("/api/v1.0/precipitation")
def names():
    """Return a list of Measurement Dates & Precipitation"""
    # Query Measurement data 
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()

    # Create a dictionary from the row data and append to a list of precipitation data
    precip_data = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["Precipitation"] = prcp
        precip_data.append(precip_dict)

    return jsonify(precip_data)


@app.route("/api/v1.0/stations")
def names():
    """Return a list of all station names"""
    # Return a JSON list of stations from the dataset
    session = Session(engine)
    stations = session.query(Station.name).all()

    # Convert list of tuples into normal list
    station_names = list(np.ravel(stations))

    return jsonify(station_names)


@app.route("/api/v1.0/tobs")
def tobs():
    # Query
    session = Session(engine)

    end_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    prev_year = (dt.datetime.strptime(end_date, '%Y-%m-%d') - dt.timedelta(days=365)

    tobs_query = session.query(Measurement.tobs).filter(Measurement.date >= prev_year).all()

    tobs_results = list(np.ravel(tobs_query))

    return jsonify(tobs_results)


    if __name__ == '__main__':
        app.run(debug=True)

