#!/bin/bash

service dbus start
bluetoothd &

python3 runMibandApi.py
