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
    'db' : 'user_dtb',
    'host' : 'localhost',
    'port' : '5432'
}

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

db = SQLAlchemy(app)
migrate = Migrate(app, db, directory='./user_database/migrations')
manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host='localhost', port=5000))

from user_database import routes