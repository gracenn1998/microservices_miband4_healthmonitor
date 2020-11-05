from flask import jsonify
from miband4_api import app
import argparse
import subprocess
import time
from datetime import datetime, timedelta

from bluepy.btle import BTLEDisconnectError
from miband4.miband import miband

from miband4_api import global_var


@app.route("/")
def hello():
    return jsonify(global_var.logged_data)


@app.route("/disconnect")
def disconnect():
    global_var.band.disconnect()
    return 'Disconnected'


@app.route("/access/<mac_add>/<auth_key>") #-> get, post method
def connect(mac_add, auth_key):
    # global band
    #if already connected
    band = global_var.band
    if(band is not None):
        return 'This device has been paired. Unpair?'
            
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
    if auth_key:
        auth_key_byte = bytes.fromhex(auth_key)
    success = False
    while not success:
        try:
            if (auth_key):
                global_var.band = miband(mac_add, auth_key_byte, debug=True)
                success = global_var.band.initialize()
                global_var.mac_add = mac_add
                global_var.auth_key = auth_key
            else:
                global_var.band = miband(mac_add, debug=True)
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
    return 'Successfully paired'


@app.route('/getinfo')
def get_device_info():
    #if paired
    band = global_var.band
    return jsonify(software_revision=band.get_revision(),
                    hardware_revision=band.get_revision(),
                    serial=band.get_serial(),
                    battery=band.get_battery_info()['level'],
                    mac_address=global_var.mac_add,
                    auth_key=global_var.auth_key,
                    time=band.get_current_time()['date'].isoformat())
    

@app.route("/heartrate/once")
def get_heartrate_once():
    # global band
    return jsonify(hearrate_once=global_var.band.get_heart_rate_one_time())



@app.route('/getsteps')
def get_step_count():
    #require device connected status
    #if not -> redirect: access

    #if connected
    # global band
    # global_var.band = global_var.band
    binfo = global_var.band.get_steps()
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
    global_var.logged_data[timestamp.strftime('%d.%m.%Y - %H:%M')] = single_row
    if(timestamp > global_var.logged_tstamp - timedelta(minutes=1)):
        global_var.finished_log = True
    print("{}: category: {}; intensity {}; steps {}; heart rate {};\n".format( timestamp.strftime('%d.%m - %H:%M'), c, i ,s ,h))

@app.route('/logdata')
def get_activity_logs():
    #gets activity log for this day
    temp = datetime.now()
    # start = datetime(year=2020, month=1, day=31, hour=0, minute=00)
    # end = datetime(year=2020, month=1, day=31, hour=11, minute=59)
    global_var.logged_tstamp = temp

    global_var.band.get_activity_betwn_intervals(datetime(temp.year,temp.month,temp.day), temp, activity_log_callback)
    # global_var.band.get_activity_betwn_intervals(start, end, activity_log_callback)
    while not global_var.finished_log:
        global_var.band.waitForNotifications(0.2)

    return global_var.logged_data

