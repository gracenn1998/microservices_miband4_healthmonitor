from user_database import app, db
from flask import request, jsonify
from user_database.models import User
import datetime
import os, hashlib


@app.route('/adduser', methods=['POST'])
def add_user():
    user = request.json
    email = user['email']
    
    pw = user['password']
    salt = os.urandom(32)
    hashed_pw = hashlib.pbkdf2_hmac(
        'sha256',
        pw.encode('utf-8'),
        salt,
        100000,
        dklen=128
    )

    try:
        new_user = User(password_hashed=hashed_pw, email=email, password_salt=salt)
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        return str(e)

    return jsonify(new_user.serialize())


@app.route('/getuser/<email>')
def getuser(email):
    try:
        user = User.query.filter_by(email=email).first()
        if(user):
            return jsonify({'user': user.serialize()})
        return jsonify({'user':None})
    except Exception as e:
        return str(e)


@app.route('/updateuser/<email>', methods=['PUT'])
def updateuser(email):
    try:
        userdata = request.json
        fullname = userdata['fullname']
        gender = userdata['gender']
        dob = datetime.datetime.strptime(userdata['dob'],"%d.%m.%Y")
        user = User.query.filter_by(email=email).first()
        user.fullname = fullname
        user.gender = gender
        user.dob = dob
        db.session.commit()
        return jsonify(user.serialize())
    except Exception as e:
        return str(e)


@app.route('/changepassword/<email>', methods=['PUT'])
def change_password(email):
    try:
        pw = request.json['password']
        salt = os.urandom(32)
        hashed_pw = hashlib.pbkdf2_hmac(
            'sha256',
            pw.encode('utf-8'),
            salt,
            100000,
            dklen=128
        )

        user = User.query.filter_by(email=email).first()
        user.password_hashed = hashed_pw
        user.password_salt = salt
        db.session.commit()
        return jsonify(user.serialize())
    except Exception as e:
        return str(e)


@app.route('/checkpassword/<email>', methods=['POST'])
def check_password(email):
    try:
        user = User.query.filter_by(email=email).first()
        salt = user.password_salt
        pw_to_check = request.json['password']

        hashed_pw = hashlib.pbkdf2_hmac(
            'sha256',
            pw_to_check.encode('utf-8'),
            salt,
            100000,
            dklen=128
        )

        if(hashed_pw == user.password_hashed):
            return jsonify({
                'result': 'correct'
            })
        return jsonify({
            'result': 'incorrect'
        })
    except Exception as e:
        return str(e)


@app.route('/deleteuser/<email>')
def delete_user(email):
    try:
        user = User.query.filter_by(email=email).first()
        db.session.delete(user)
        db.session.commit()
        return 'Deleted'
    except Exception as e:
        return str(e)

