from database import app
from flask import request, jsonify
import datetime

from database.models import Miband4, ActivityRecord

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/addband")
def add_band():
    serial = request.args.get('serial')
    sw_rev = request.args.get('sw_rev')
    hw_rev = request.args.get('hw_rev')
    mac = request.args.get('mac')
    auth = request.args.get('auth')
    try:
        band=Miband4(
            serial = serial,
            software_revision = sw_rev,
            hardware_revision = hw_rev,
            mac_address = mac,
            auth_key = auth
        )
        db.session.add(band)
        db.session.commit()
        return "Band added. Band id={}".format(band.id)
    except Exception as e:
	    return(str(e))

@app.route("/getallband")
def get_all_bands():
    try:
        bands=Miband4.query.all()
        return  jsonify([band.serialize() for band in bands])
    except Exception as e:
	    return(str(e))

@app.route("/getband/<id_>")
def get_band_by_id(id_):
    try:
        band=Miband4.query.filter_by(id=id_).first()
        return jsonify(band.serialize())
    except Exception as e:
	    return(str(e))


@app.route("/addlogs", methods=['POST'])
def add_logs():
    # logs = request.args.get[logs]
    band_id = request.args.get('band_id')
    logs = request.json
    for ts in logs:
        # timestamp = time
        timestamp = datetime.datetime.strptime(ts,"%d.%m.%Y - %H:%M")
        intensity = logs[ts]['intensity']
        steps = logs[ts]['steps']
        heartrate = logs[ts]['heartrate']
        category = logs[ts]['category']
        try:
            log=ActivityRecord(
                band_id = band_id,
                timestamp = timestamp,
                intensity = intensity,
                steps = steps,
                heartrate = heartrate,
                category = category
            )
            db.session.add(log)
        except Exception as e:
            print(e)
            # return(str(e)
    db.session.commit()
    return "Logs added"

@app.route("/getalllogs")
def get_all_logs():
    try:
        logs=ActivityRecord.query.all()
        return  jsonify([log.serialize() for log in logs])
    except Exception as e:
	    return(str(e))


@app.route("/getlogs/<band_id>")
def get_log_of(band_id):
    try:
        logs=ActivityRecord.query.filter_by(band_id=band_id)
        return jsonify([log.serialize() for log in logs])
    except Exception as e:
        return(str(e))

if __name__ == '__main__':
    app.run(debug=True)