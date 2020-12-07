from miband4_database import app, db
from flask import request, jsonify
import datetime

from miband4_database.models import Miband4, ActivityRecord

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/bands", methods=['POST'])
def add_band():
    bandinfo = request.json
    serial = bandinfo['serial']
    sw_rev = bandinfo['software_revision']
    hw_rev = bandinfo['hardware_revision']
    mac = bandinfo['mac_add']
    auth = bandinfo['auth_key']
    userid = bandinfo['uid']
    try:
        band=Miband4(
            serial = serial,
            software_revision = sw_rev,
            hardware_revision = hw_rev,
            mac_address = mac,
            auth_key = auth,
            uid = userid
        )
        db.session.add(band)
        db.session.commit()
        return jsonify({
            'add-band-result': 'succeeded',
            'band-info': band.serialize()
        })
    except Exception as e:
	    return(str(e))

# @app.route("/getallband")
# def get_all_bands():
#     try:
#         bands=Miband4.query.all()
#         return  jsonify([band.serialize() for band in bands])
#     except Exception as e:
# 	    return(str(e))

@app.route("/bands/<id>")
def get_band_by_id(id):
    try:
        band=Miband4.query.filter_by(id=id).first()
        return jsonify(band.serialize())
    except Exception as e:
	    return(str(e))

@app.route("/bands/find-by-userid")
def get_band_by_user():
    uid = request.args.get('uid')
    try:
        band=Miband4.query.filter_by(uid=uid).first()
        return jsonify(band.serialize())
    except Exception as e:
	    return(str(e))


@app.route("/bands/<id>/logs", methods=['POST'])
def add_logs(id):
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
                band_id = id,
                timestamp = timestamp,
                intensity = intensity,
                steps = steps,
                heartrate = heartrate,
                category = category
            )
            db.session.add(log)
            response = jsonify({
                'add-logs-result' : 'succeeded',
            })
        except Exception as e:
            print(e)
            response = jsonify({
                'add-logs-result' : 'failed',
            })
    
    db.session.commit()
    return response

# @app.route("/getalllogs")
# def get_all_logs():
#     try:
#         logs=ActivityRecord.query.all()
#         return  jsonify([log.serialize() for log in logs])
#     except Exception as e:
# 	    return(str(e))


@app.route("/bands/<id>/logs")
def get_log_of(id):
    try:
        logs=ActivityRecord.query.filter_by(band_id=id)
        serializedLogs = []
        for log in logs:
            serializedLogs.append(log.serialize()) 
        response = jsonify({
            'logs': serializedLogs,
            'get-logs-result': 'succeeded'
        })
    except Exception as e:
        response = jsonify({'get-logs-result': 'failed'})
        print(e)
    
    return response
    


@app.route("/bands/<id>/logs/get-by-time")
def get_log_by_timestamp_of(id):
    start = request.args.get('start')
    end = request.args.get('end')
    start = datetime.datetime.strptime(start, "%d.%m.%Y - %H:%M")
    end = datetime.datetime.strptime(end, "%d.%m.%Y - %H:%M")
    try:
        logs=ActivityRecord.query.filter_by(band_id=id)\
                                .filter(ActivityRecord.timestamp.between(start, end))
        serializedLogs = []
        for log in logs:
            serializedLogs.append(log.serialize()) 
        response = jsonify({
            'logs': serializedLogs,
            'get-logs-result': 'succeeded'
        })
    except Exception as e:
        response = jsonify({'get-logs-result': 'failed'})
    
    return response

@app.route("/bands/<id>/last-fetch-time")
def get_last_fetch_time_of(id):
    try:
        band=Miband4.query.filter_by(id=id).first()
        last_ts = band.last_fetch_data_timestamp
        if(last_ts==None):
            last_ts=''
        response = jsonify({
            'get-timestamp-result': 'succeeded',
            'last-fetch-timestamp': last_ts
        })
    except Exception as e:
        response = jsonify({'get-timestamp-result': 'failed'})
        print(e)
    
    return response

@app.route("/bands/<id>/last-fetch-time", methods=['POST'])
def set_last_time_of(id):
    data = request.json
    last_ts = datetime.datetime.strptime(data['last'], "%d.%m.%Y - %H:%M")
    try:
        band=Miband4.query.filter_by(id=id).first()
        band.last_fetch_data_timestamp = last_ts
        db.session.commit()
        response = jsonify({
            'set-timestamp-result': 'succeeded'
        })
    except Exception as e:
        response = jsonify({'get-timestamp-result': 'failed'})
        print(e)
    
    return response


@app.route('/bands/<id>', methods=['DELETE'])
def delete_band(id):
    try:
        band = Miband4.query.filter_by(id=id).delete()
        db.session.delete(band)
        db.session.commit()
        return jsonify({
            'delete-result': 'succeeded'
        })
    except Exception as e:
        return str(e)

@app.route('/bands/<id>/logs', methods=['DELETE'])
def delete_logs_of(bandid):
    try:
        logs=ActivityRecord.query.filter_by(band_id=bandid).delete()
        db.session.commit()
        return jsonify({
            'delete-result': 'succeeded'
        })
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)