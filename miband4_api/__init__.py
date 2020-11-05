from flask import Flask, jsonify, session
from miband4_api import global_var


global_var.init()
app = Flask(__name__)


from miband4_api import routes
