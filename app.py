import numpy as np
from numpy.testing._private.utils import measure

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from sqlalchemy import inspect
from flask import Flask, json, jsonify

# Database Setup
#################################################
engine = create_engine("sqlite:///./Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect = True)

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app= Flask(__name__)


@app.route("/")
def home():
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0<br/>"
        f"/api/v1.0/precipiation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )
 
@app.route("/api/v1.0/precipiation/")
def precipitation():
    print("Precipitation")
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    one_year_ago = dt.datetime.strptime(recent_date, '%Y-%m-%d')- dt.timedelta(days = 365)

    prcp_results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= one_year_ago).\
    order_by(Measurement.date).all()

    prcp_dictionary = dict(prcp_results)
    print(f"Results {prcp_dictionary} ")
    return jsonify(prcp_dictionary)

@app.route("/api/v1.0/stations/")
def stations():
    print("Stations")
    station_list= session.query(Station.station).order_by(Station.station).all()

    station_names = list(np.ravel(station_list))
    return jsonify(station_names)

@app.route("/api/v1.0/tobs/")
def tobs():
    print("tobs")
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    one_year_ago = dt.datetime.strptime(recent_date, '%Y-%m-%d')- dt.timedelta(days = 365)   
    
    active_station = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station=="USC00519281")\
    .filter(Measurement.date >= one_year_ago).order_by(Measurement.date).all()
    tobs_list = list(np.ravel(active_station))
    return jsonify(tobs_list)

app.route("/api/v1.0/start/<start>/")
def start(start):
    print("start date: start")
    start = time.strptime(start, '%Y-%m-%d')
    measures = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
    .filter(Measurement.date >= start).all()
    print(measures)
    return jsonify(measures)

app.route("/api/v1.0/start_end/<start>/<end>")
def start_end(start, end):
    print("start & end date")
    start = time.strptime(start, '%Y-%m-%d')
    end = time.strptime(end, '%Y-%m-%d')
    measures = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
    .filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    print(measures)
    return jsonify(measures)
    



if __name__ == "__main__":
    app.run(debug=True)