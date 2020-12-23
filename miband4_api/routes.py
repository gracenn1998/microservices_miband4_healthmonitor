from flask import jsonify, request, session
from miband4_api import app, globals
import argparse
import subprocess
import time
from datetime import datetime, timedelta

from bluepy.btle import BTLEDisconnectError
from miband4.miband import miband



def connect(mac_add, auth_key):
    band = None
    if auth_key:
        auth_key_byte = bytes.fromhex(auth_key)
    success = False
    maxTry=3
    i=0
    while (not success) and (i < maxTry) :
        try:
            i+=1
            if (auth_key):
                band = miband(mac_add, auth_key_byte, debug=True)
                success = band.initialize()
            break
        except BTLEDisconnectError:
            #show in browser?
            print('Connection to the MIBand failed. Trying out again in 3 seconds')
            time.sleep(3)
            continue
        except KeyboardInterrupt: #close browser?
            print("\nExit.")
            exit()
        except Exception as e:
            print(e)
            break
    if(not success): return None

    # if succeeded
    return band

@app.route("/band/connect", methods=['POST'])
def get_mac_and_key():
    # global band
    #if already connected
    info = request.json
    mac_add = info['mac_add']
    auth_key = info['auth_key']
    
    try: 
        globals.band = connect(mac_add, auth_key)
    except Exception as e:
        print(e)
        return jsonify({
            'connect-result': 'failed'
        })
    if(globals.band) : #if band is not none -> paired
        band = globals.band
        bandinfo = {
            'software_revision': band.get_revision(),
            'hardware_revision': band.get_revision(),
            'serial': band.get_serial(),
            'battery': band.get_battery_info()['level'],
            'time': band.get_current_time()['date'].isoformat()
        }
        response = jsonify({
            'connect-result': 'succeeded',
            'band-info': bandinfo
        })
    else:
        response = jsonify({
            'connect-result': 'failed'
        })  

    return response 
 

@app.route('/band/disconnect')
def disconnect():
    try:
        if(globals.band):
            globals.band.disconnect()
            globals.band = None
            response = jsonify({
                'disconnect-result': 'succeeded'
            })
        else:
            response = jsonify({
                'disconnect-result': 'failed'
            })
    except Exception as e:
        print(e)
        return '', 500

    return response



@app.route('/band/info')
def get_band_info():
    try:
        if(globals.band):
            band = globals.band
            bandinfo = {
                'software_revision': band.get_revision(),
                'hardware_revision': band.get_revision(),
                'serial': band.get_serial(),
                'battery': band.get_battery_info()['level'],
                'time': band.get_current_time()['date'].isoformat()
            }

            # band.disconnect()
            response= jsonify({
                'get-info-result': 'succeeded',
                'band-info': bandinfo
            })
        else:
            response = jsonify({
                'get-info-result': 'failed'
            })
    except Exception as e:
        print(e)
        return '', 500

    return response
    

@app.route('/band/general')
def get_step_count():
    try:
        if(globals.band):    
            stepinfo = globals.band.get_steps()
            response = jsonify({
                'get-step-result': 'succeeded',
                'stepinfo': stepinfo
            })
        else:
            response = jsonify({
                'get-step-result': 'failed'
            })
    except Exception as e:
        print(e)
        return '', 500

    return response


def activity_log_callback(timestamp,c,i,s,h):
    globals.now_ts = timestamp
    print('log')
    single_row = {
        'category' : c,
        'intensity' : i,
        'steps' : s,
        'heartrate' : h
        }
    globals.logged_data[timestamp.strftime('%d.%m.%Y - %H:%M')] = single_row
    # print('fetching...')
    if(timestamp >= globals.end_log_ts - timedelta(minutes=1)):
        globals.finish_flag = True
    print("{}: category: {}; intensity {}; steps {}; heart rate {};\n".format( timestamp.strftime('%d.%m - %H:%M'), c, i ,s ,h))


@app.route('/band/activitydata')
def get_activity_logs():
    try:
        if(globals.band):
            globals.finish_flag = False
            globals.logged_data = {}
            # info = request.json
            start = request.args.get('start')
            end = request.args.get('end')
            start = datetime.strptime(start, "%d.%m.%Y - %H:%M")
            end = datetime.strptime(end, "%d.%m.%Y - %H:%M")
            
            globals.end_log_ts = end
            globals.band.get_activity_betwn_intervals(start, end, activity_log_callback)
            while not globals.finish_flag:
                globals.band.waitForNotifications(0.5)

            response = jsonify({
                'log-data-result': 'succeeded',
                'logs': globals.logged_data
            })
        
        else:
            response = jsonify({
                'log-data-result': 'failed'
            })
    except Exception as e:
        print(e)
        return '', 500
        
    globals.logged_data = {}
    return response
