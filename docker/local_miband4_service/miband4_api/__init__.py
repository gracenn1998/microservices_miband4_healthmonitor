from flask import Flask, jsonify, session
import os
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

app.secret_key = os.urandom(32)

from miband4_api import routes


