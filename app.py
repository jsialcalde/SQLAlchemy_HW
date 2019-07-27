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

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br>"
        f"/api/v1.0/start/end<br>"
        f"Dates are in the format %Y-%m-%d"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Convert the query results to a Dictionary using date as the key and prcp as the value."""
    # Query 
    session = Session(engine)
    

    selMeasurement = [Measurement.date]

    StationTemp = session.query(*selMeasurement,func.sum(Measurement.prcp))\
        .group_by(Measurement.date).order_by(Measurement.date.desc()).all()

    return jsonify(StationTemp)


@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""

    session = Session(engine)
    
#     selMeasurement = [Measurement.id, Measurement.station, Measurement.date,Measurement.prcp,Measurement.tobs]
    selMeasurement = [Measurement.station]
    stations = session.query(*selMeasurement)\
        .group_by(Measurement.station).all()


    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
#     """Return a JSON list of Temperature Observations (tobs) for the previous year."""
    session = Session(engine)
    selMeasurement = [Measurement.date]
    
    StationTemp = session.query(*selMeasurement, func.avg(Measurement.tobs)).filter(Measurement.date >= '2016-08-18')\
    .filter(Measurement.date <= '2017-08-18')\
    .group_by(Measurement.date)\
    .order_by(Measurement.date.desc()).all()

    return jsonify(StationTemp)



@app.route("/api/v1.0/<start>")
def TempStart(start):
#     """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start."""

    """Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d """
    
    session = Session(engine)
    selMeasurement = [Measurement.date]
    
    Temps = session.query(*selMeasurement, func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start)\
    .group_by(Measurement.date)\
    .order_by(Measurement.date.desc()).all()


    return jsonify(Temps)


@app.route("/api/v1.0/<start>/<end>")
def TempStartEnd(start,end):
#     """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start-end range."""

    """Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d """
    
    session = Session(engine)
    selMeasurement = [Measurement.date]
    
    Temps = session.query(*selMeasurement, func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start)\
    .filter(Measurement.date <= end).group_by(Measurement.date)\
    .order_by(Measurement.date.desc()).all()


    return jsonify(Temps)

if __name__ == '__main__':
    app.run(debug=True)