from flask import jsonify, request, session
from miband4_api import app
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
    while not success:
        try:
            if (auth_key):
                band = miband(mac_add, auth_key_byte, debug=True)
                success = band.initialize()
                mac_add = mac_add
                auth_key = auth_key
            else:
                band = miband(mac_add, debug=True)
                success = True
            break
        except BTLEDisconnectError:
            #show in browser?
            print('Connection to the MIBand failed. Trying out again in 3 seconds')
            time.sleep(3)
            continue
        except KeyboardInterrupt: #close browser?
            print("\nExit.")
            exit()
    session['mac_add'] = mac_add
    session['auth_key'] = auth_key
    return band

@app.route("/connect", methods=['POST'])
def get_mac_and_key():
    # global band
    #if already connected
    info = request.json
    mac_add = info['mac_add']
    auth_key = info['auth_key']
    band = connect(mac_add, auth_key)
    # if(band is not None):
    #     return 'This device has been paired. Unpair?'
            
    #if not connected yet
    #check to see if dtb has already had the data or not
    #....
    #if yes -> get data from dtb
    #if no data in dtb -> post method data -> another route
    #Validate mac
    #....
    #Validate key
    #....
    #Convert Auth Key from hex to byte format
    band.disconnect()
    return 'Successfully paired. Mac address and auth key are correct'


@app.route('/getinfo')
def get_device_info():
    #require mac&auth in session
    #if not -> redirect: connect

    #if mac in session
    mac_add = session['mac_add']
    auth_key = session['auth_key']
    band = connect(mac_add, auth_key)
    respone = jsonify(software_revision=band.get_revision(),
                    hardware_revision=band.get_revision(),
                    serial=band.get_serial(),
                    battery=band.get_battery_info()['level'],
                    mac_address=session['mac_add'],
                    auth_key=session['auth_key'],
                    time=band.get_current_time()['date'].isoformat())
    band.disconnect()
    return respone 
    

@app.route("/heartrate/once")
def get_heartrate_once():
    #require mac&auth in session
    #if not -> redirect: connect

    #if mac in session
    mac_add = session['mac_add']
    auth_key = session['auth_key']
    band = connect(mac_add, auth_key)

    response = jsonify(hearrate_once=band.get_heart_rate_one_time())
    band.disconnect()
    return response



@app.route('/getsteps')
def get_step_count():
    #require mac&auth in session
    #if not -> redirect: connect
    
    #if mac in session
    mac_add = session['mac_add']
    auth_key = session['auth_key']
    band = connect(mac_add, auth_key)
    
    binfo = band.get_steps()
    band.disconnect()
    return jsonify(steps=binfo['steps'],
                    fat_burned=binfo['fat_burned'],
                    calories=binfo['calories'],
                    travelled_distance=binfo['meters'])


def activity_log_callback(timestamp,c,i,s,h):
    single_row = {
        'category' : c,
        'intensity' : i,
        'steps' : s,
        'heartrate' : h
        }
    session['logged_data'][timestamp.strftime('%d.%m.%Y - %H:%M')] = single_row
    print('fetching...')
    if(timestamp >= session['logged_tstamp'] - timedelta(minutes=1)):
        session['finished_log'] = True
    print("{}: category: {}; intensity {}; steps {}; heart rate {};\n".format( timestamp.strftime('%d.%m - %H:%M'), c, i ,s ,h))

@app.route('/logdatatoday')
def get_activity_logs_today():
    #require mac&auth in session
    #if not -> redirect: connect
    
    #if mac in session
    mac_add = session['mac_add']
    auth_key = session['auth_key']
    band = connect(mac_add, auth_key)

    session['finished_log'] = False
    session['logged_data'] = {}
    #gets activity log for this day
    temp = datetime.now()
    session['logged_tstamp'] = temp

    band.get_activity_betwn_intervals(datetime(temp.year,temp.month,temp.day), temp, activity_log_callback)
    while not session['finished_log']:
        print('wait')
        band.waitForNotifications(0.2)

    band.disconnect()
    return session['logged_data']


@app.route('/logdata', methods=['POST'])
def get_activity_logs():
    #require mac&auth in session
    #if not -> redirect: connect
    
    #if mac in session
    mac_add = session['mac_add']
    auth_key = session['auth_key']
    band = connect(mac_add, auth_key)

    session['finished_log'] = False
    session['logged_data'] = {}
    info = request.json
    start = datetime.strptime(info['start'], "%d.%m.%Y - %H:%M")
    end = datetime.strptime(info['end'], "%d.%m.%Y - %H:%M")
    
    session['logged_tstamp'] = end
    band.get_activity_betwn_intervals(start, end, activity_log_callback)
    while not session['finished_log']:
        print('wait')
        band.waitForNotifications(0.2)

    band.disconnect()
    return session['logged_data']
