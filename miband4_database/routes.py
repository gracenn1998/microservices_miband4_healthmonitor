from miband4_database import app, db
from flask import request, jsonify
import datetime

from miband4_database.models import Miband4, ActivityRecord

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/addband", methods=['POST'])
def add_band():
    bandinfo = request.json
    serial = bandinfo['serial']
    sw_rev = bandinfo['software_revision']
    hw_rev = bandinfo['hardware_revision']
    mac = bandinfo['mac_address']
    auth = bandinfo['auth_key']
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

# @app.route("/getallband")
# def get_all_bands():
#     try:
#         bands=Miband4.query.all()
#         return  jsonify([band.serialize() for band in bands])
#     except Exception as e:
# 	    return(str(e))

@app.route("/getband/<id>")
def get_band_by_id(id):
    try:
        band=Miband4.query.filter_by(id=id).first()
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

# @app.route("/getalllogs")
# def get_all_logs():
#     try:
#         logs=ActivityRecord.query.all()
#         return  jsonify([log.serialize() for log in logs])
#     except Exception as e:
# 	    return(str(e))


@app.route("/getalllogs/<band_id>")
def get_log_of(band_id):
    try:
        logs=ActivityRecord.query.filter_by(band_id=band_id)
        return jsonify([log.serialize() for log in logs])
    except Exception as e:
        return(str(e))


@app.route("/getlogsbytime/<band_id>", methods=['POST'])
def get_log_by_timestamp_of(band_id):
    info = request.json
    start = datetime.datetime.strptime(info['start'], "%d.%m.%Y - %H:%M")
    end = datetime.datetime.strptime(info['end'], "%d.%m.%Y - %H:%M")
    try:
        logs=ActivityRecord.query.filter_by(band_id=band_id)\
                                .filter(ActivityRecord.timestamp.between(start, end))
        return jsonify([log.serialize() for log in logs])
    except Exception as e:
        return(str(e))

if __name__ == '__main__':
    app.run(debug=True)