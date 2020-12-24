from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


POSTGRES = {
    'user' : 'postgres',
    'pw' : '123123',
    'db' : 'health_monitor_system',
    'host' : 'localhost',
    'port' : '5430'
}

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

db = SQLAlchemy(app)
from database_construct.models import User, Miband4, ActivityRecord
migrate = Migrate(app, db, directory='./database_construct/migrations')
manager = Manager(app)

manager.add_command('db', MigrateCommand)