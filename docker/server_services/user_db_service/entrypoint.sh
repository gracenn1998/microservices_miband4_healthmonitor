#!/bin/ash
python3 runUserDbApi.py db upgrade
python3 runUserDbApi.py runserver
