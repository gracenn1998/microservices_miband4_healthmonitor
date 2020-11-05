from flask import Flask, jsonify, session
from miband4_flask import global_var


global_var.init()
app = Flask(__name__)


from miband4_flask import routes