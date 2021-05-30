import numpy as np

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
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )
 
@app.route("/api/v1.0/precipiation/")
def precipitation():
    print("Precipitation")
    session = Session(engine)
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    one_year_ago = dt.datetime.strptime(recent_date, '%Y-%m-%d')- dt.timedelta(days = 365)

    prcp_results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= one_year_ago).\
    order_by(Measurement.date).all()

    prcp_dictionary = dict(prcp_results)
    print(f"Results {prcp_dictionary} ")
    return jsonify(prcp_dictionary)

if __name__ == "__main__":
    app.run(debug=True)