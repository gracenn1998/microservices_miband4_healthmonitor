from flask import Flask, jsonify, session
import os


app = Flask(__name__)
app.secret_key = os.urandom(32)

from miband4_api import routes


