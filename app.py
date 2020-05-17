import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
Stations= Base.classes.station
Measurements=Base.classes.measurement


app=Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)
#   * Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
    results = session.query(Measurements.date, Measurements.prcp).all()
    session.close()
    alist = []
    for date, prcp in results:
        adict={}
        adict["date"]=date
        adict["Precipitation"]= prcp
        alist.append(adict)
        
# jsonify it
    return jsonify(alist)

@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)
#   * Return a JSON list of stations from the dataset.
    results = session.query(Stations.station).all()

    session.close()
# jsonify it
    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
#   * Query the dates and temperature observations of the most active station for the last year of data.
    session= Session(engine)
    year_ago ='2016-08-23'
    results = session.query(Measurements.date, Measurements.tobs).filter(Measurements.date>=year_ago, Measurements.station=='USC00519281').all()
    session.close()

#   * Return a JSON list of temperature observations (TOBS) for the previous year.
    return jsonify(results)
@app.route("/api/v1.0/<start>")
def startend(start):
# * `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`
    session = Session(engine)
    # start_date = start.replace(" ").lower()
    results = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).filter(Measurements.date >= start).all()
    returnvalue = {}
    returnvalue['maximum'] = results[0][2]
    returnvalue['minimum'] = results[0][0]
    returnvalue['average'] = results[0][1]
    return jsonify(returnvalue)
    # for row in Measurements:
    #     new_date = Measurements['start'].replace(" ", " ").lower()
    #     if new_date >= start_date:
    #         return jsonify()
@app.route("/api/v1.0/<start>/<end>")
def end(start, end):
# * `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`
    session = Session(engine)
    # start_date = start.replace(" ").lower()
    results = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).filter(Measurements.date >= start).filter(Measurements.date <= end).all()
    returnvalue = {}
    returnvalue['maximum'] = results[0][2]
    returnvalue['minimum'] = results[0][0]
    returnvalue['average'] = results[0][1]
    return jsonify(returnvalue)

    # 2016-08-23
#   * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

#   * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

#   * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

if __name__ == "__main__":
    app.run(debug=True)