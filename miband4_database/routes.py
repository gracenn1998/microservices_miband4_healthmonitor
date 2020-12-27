from miband4_database import app, db
from flask import request, jsonify
import datetime

from database_construct.models import Miband4, ActivityRecord

@app.route("/v1/")
def hello():
    return "Hello World!"

@app.route("/v1/bands", methods=['POST'])
def add_band():
    bandinfo = request.json
    serial = bandinfo['serial']
    sw_rev = bandinfo['software_revision']
    hw_rev = bandinfo['hardware_revision']
    mac = bandinfo['mac_address']
    auth = bandinfo['auth_key']
    userid = bandinfo['user_id']
    try:
        band=Miband4(
            serial = serial,
            software_revision = sw_rev,
            hardware_revision = hw_rev,
            mac_address = mac,
            auth_key = auth,
            user_id = userid,
            last_fetch_data_timestamp = datetime.datetime.now()
        )
        db.session.add(band)
        db.session.commit()
        response = jsonify({
            'add-band-result': 'succeeded',
            'band-info': band.serialize()
        })
    except Exception as e:
        print(e)
        return '', 500

    return response



@app.route("/v1/bands/<id>/update-new-user", methods=['PUT'])
def update_band_user(id):
    bandinfo = request.json
    sw_rev = bandinfo['software_revision']
    hw_rev = bandinfo['hardware_revision']
    mac = bandinfo['mac_address']
    auth = bandinfo['auth_key']
    userid = bandinfo['user_id']
    try:
        band=Miband4.query.filter_by(id=id).first()
        band.software_revision = sw_rev
        band.hardware_revision = hw_rev
        band.mac_address = mac
        band.auth_key = auth
        band.user_id = userid
        band.last_fetch_data_timestamp = datetime.datetime.now()
        db.session.commit()
        response = jsonify({
            'add-band-result': 'succeeded',
            'band-info': band.serialize()
        })
    
    except Exception as e:
        print(e)
        return '', 500

    return response

@app.route("/v1/bands/<id>/unpair")
def unpair_band(id):
    try:
        band=Miband4.query.filter_by(id=id).first()
        band.user_id = None
        db.session.commit()
        response = jsonify({
            'unpair-band-result': 'succeeded',
        })
    
    except Exception as e:
        print(e)
        return '', 500

    return response

# @app.route("/v1/getallband")
# def get_all_bands():
#     try:
#         bands=Miband4.query.all()
#         return  jsonify([band.serialize() for band in bands])
#     except Exception as e:
# 	    return(str(e))

@app.route("/v1/bands/<id>")
def get_band_by_id(id):
    try:
        band=Miband4.query.filter_by(id=id).first()
        response = {
            'get-band-result': 'succeeded',
            'band-info': band.serialize()
        }
    
    except Exception as e:
        print(e)
        return '', 500

    return response

@app.route("/v1/bands/find-by-userid")
def get_band_by_user():
    uid = request.args.get('user_id')
    try:
        band=Miband4.query.filter_by(user_id=uid).first()
        if(band):
            response = jsonify({
                'get-band-result': 'succeeded',
                'band-info': band.serialize()
            })
        else: return '',204
    
    except Exception as e:
        print(e)
        return '', 500

    return response

@app.route("/v1/bands/find-by-serial")
def get_band_by_serial():
    serial = request.args.get('serial')
    try:
        band=Miband4.query.filter_by(serial=serial).first()
        if(band):
            response = jsonify({
                'get-band-result': 'succeeded',
                'band-info': band.serialize()
            })
        else: return '',204
    
    except Exception as e:
        print(e)
        return '', 500

    return response


@app.route("/v1/bands/<bid>/<uid>/logs", methods=['POST'])
def add_logs_of(uid, bid):
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
                user_id = uid,
                band_id = bid,
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
            return '', 500
    
    db.session.commit()
    return response

# @app.route("/v1/getalllogs")
# def get_all_logs():
#     try:
#         logs=ActivityRecord.query.all()
#         return  jsonify([log.serialize() for log in logs])
#     except Exception as e:
# 	    return(str(e))


@app.route("/v1/users/<uid>/logs")
def get_log_of_user(uid):
    try:
        logs=ActivityRecord.query.filter_by(user_id=uid)
        serializedLogs = []
        for log in logs:
            serializedLogs.append(log.serialize()) 
        response = jsonify({
            'logs': serializedLogs,
            'get-logs-result': 'succeeded'
        })
    
    except Exception as e:
        print(e)
        return '', 500
    
    return response
    


@app.route("/v1/users/<uid>/logs/get-by-time")
def get_log_by_timestamp_of(uid):
    start = request.args.get('start')
    end = request.args.get('end')
    start = datetime.datetime.strptime(start, "%d.%m.%Y - %H:%M")
    end = datetime.datetime.strptime(end, "%d.%m.%Y - %H:%M")
    try:
        logs=ActivityRecord.query.filter_by(user_id=uid)\
                                .filter(ActivityRecord.timestamp.between(start, end))
        serializedLogs = []
        for log in logs:
            serializedLogs.append(log.serialize()) 
        response = jsonify({
            'logs': serializedLogs,
            'get-logs-result': 'succeeded'
        })
    
    except Exception as e:
        print(e)
        return '', 500
    
    return response

@app.route("/v1/bands/<id>/last-fetch-time")
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
        print(e)
        return '', 500
    
    return response

@app.route("/v1/bands/<id>/last-fetch-time", methods=['POST'])
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
        print(e)
        return '', 500
    
    return response


# @app.route('/bands/<id>', methods=['DELETE'])
# def delete_band(id):
#     try:
#         band = Miband4.query.filter_by(id=id).delete()
#         db.session.delete(band)
#         db.session.commit()
#         response = jsonify({
#             'delete-result': 'succeeded'
#         })
#     except Exception as e:
#         response = jsonify({
#             'delete-result': 'failed'
#         })
    
#     return response

@app.route('/users/<userid>/logs', methods=['DELETE'])
def delete_logs_of(userid):
    try:
        logs=ActivityRecord.query.filter_by(user_id=userid).delete()
        db.session.commit()
        response = jsonify({
            'delete-result': 'succeeded'
        })
    
    except Exception as e:
        print(e)
        return '', 500
    
    return response

@app.route("/v1.1/bands/new-upgrade")
def new_upgrade():
    return 'This is new api after upgrading'