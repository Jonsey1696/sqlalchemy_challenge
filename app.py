import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect = True)
Measurement=Base.classes.measurement
Station=Base.classes.station

app = Flask(__name__)


@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Welcome to the Climate API<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/YYYY-MM-DD<br/>"
        f"/api/v1.0/YYYY-MM-DD/YYYY-MM-DD"
    )

@app.route("/api/v1.0/precipitation")
def rain():
    session= Session(engine)
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results=session.query(Measurement.date, Measurement.prcp).filter(Measurement.date.between(query_date, "2017-8-23")).all()
    session.close()

    all_prcp_dates=[]
    for date, prcp in results:
        rain_dict={}
        rain_dict["date"]=date
        rain_dict["prcp"]=prcp
        all_prcp_dates.append(rain_dict)

    return jsonify(all_prcp_dates)

@app.route("/api/v1.0/stations")
def stations():
    session=Session(engine)
    stations = session.query(Station.name).filter(Measurement.station == Station.station).group_by(Measurement.station).all()
    session.close()
    station_list=list(np.ravel(stations))
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def temps():
    session=Session(engine)
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temp_result=session.query(Measurement.tobs).filter(Measurement.date.between(query_date, "2017-8-23")).filter(Measurement.station == "USC00519281").all()
    session.close()
    temp_list=list(np.ravel(temp_result))
    return jsonify(temp_list)

@app.route("/api/v1.0/<start_date>")
def start(start_date):
    session=Session(engine)
    return_temps=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    session.close()
    return jsonify(return_temps)
    # return(start_date)

@app.route("/api/v1.0/<start_date>/<end_date>")
def range(start_date,end_date):
    session=Session(engine)
    return_temps=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    session.close()
    return jsonify(return_temps)

if __name__ == "__main__":
    app.run(debug=True)