from user_database import app, db
from flask import request, jsonify
from user_database.models import User
import datetime
import os, hashlib


@app.route('/users', methods=['POST'])
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


@app.route('/users/find-by-email')
def getuserbyemail():
    email = request.args.get('email')
    try:
        user = User.query.filter_by(email=email).first()
        if(user):
            return jsonify({'user': user.serialize()})
        return jsonify({'user':None})
    except Exception as e:
        return str(e)


@app.route('/users/<id>', methods=['PUT'])
def updateuser(id):
    try:
        userdata = request.json
        fullname = userdata['fullname']
        user = User.query.filter_by(id=id).first()
        user.fullname = fullname
        db.session.commit()
        return jsonify(user.serialize())
    except Exception as e:
        return str(e)


@app.route('/users/<id>/change-password', methods=['POST'])
def change_password(id):
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


@app.route('/users/login', methods=['POST'])
def login():
    entered_pw = request.json['password']
    email = request.json['email']
    try:
        user = User.query.filter_by(email=email).first()
        if(user): #if user with provided email exists
            salt = user.password_salt
            
            hashed_pw = hashlib.pbkdf2_hmac(
                'sha256',
                entered_pw.encode('utf-8'),
                salt,
                100000,
                dklen=128
            )

            if(hashed_pw == user.password_hashed): #if password matched
                print(jsonify({
                    'user': user.serialize(),
                    'login-result': 'succeeded'
                }))
                return jsonify({
                    'user': user.serialize(),
                    'login-result': 'succeeded'
                })
            return jsonify({ #if password unmatched
                'login-result': 'failed'
            })
        else: 
            return jsonify({ #if user with provided email doesnt exist
                'login-result': 'failed'
            })
    except Exception as e:
        return str(e)

@app.route('/users/<id>/checkpassword', methods=['POST'])
def check_password(id):
    try:
        user = User.query.filter_by(id=id).first()
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


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()
        return 'Deleted'
    except Exception as e:
        return str(e)

