#!/bin/ash
python3 runMibandDbApi.py db upgrade
python3 runMibandDbApi.py runserver
