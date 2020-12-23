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


@app.route('/users/<id>')
def getuser(id):
    try:
        user = User.query.filter_by(id=id).first()
        if(user):
            return jsonify(user.serialize())
        return '', 204 #no user found
    except Exception as e:
        return str(e)

@app.route('/users/find-by-email')
def getuserbyemail():
    email = request.args.get('email')
    try:
        user = User.query.filter_by(email=email).first()
        if(user):
            return jsonify(user.serialize())
        return '', 204 #no user found
    except Exception as e:
        print(str(e))
        return '', 500


@app.route('/users/<id>/fullname', methods=['PUT'])
def updateuser(id):
    try:
        userdata = request.json
        fullname = userdata['fullname']
        user = User.query.filter_by(id=id).first()
        user.fullname = fullname
        db.session.commit()
        return jsonify(user.serialize())
    except Exception as e:
        print(str(e))
        return '', 500


def validate_pw(user, pw):
    try:
        salt = user.password_salt
            
        hashed_pw = hashlib.pbkdf2_hmac(
            'sha256',
            pw.encode('utf-8'),
            salt,
            100000,
            dklen=128
        )

        if(hashed_pw == user.password_hashed): #if password matched
            return True
            
        return False 
    except Exception as e:
        return False

@app.route('/users/<id>/validate-password', methods=['POST'])
def check_password(id):
    try:
        user = User.query.filter_by(id=id).first()
        salt = user.password_salt
        entered_pw = request.json['password']

        if(user): #if user with provided id exists
            valid = validate_pw(user, entered_pw)
            print(valid)

        if(valid):
            response = jsonify({
                'validate-result': True
            })
        else: response = jsonify({
            'validate-result': False
        })
    except Exception as e:
        return '', 500
        print(e)
    
    return response

@app.route('/users/<id>/change-password', methods=['POST'])
def change_password(id):
    try:
        cur_pw = request.json['cur_password']
        new_pw = request.json['new_password']

        user = User.query.filter_by(id=id).first()

        if(user): #if user with provided id exists
            valid = validate_pw(user, cur_pw)

            if(valid):
                #generate new pw
                salt = os.urandom(32)
                hashed_pw = hashlib.pbkdf2_hmac(
                    'sha256',
                    new_pw.encode('utf-8'),
                    salt,
                    100000,
                    dklen=128
                )

                #update new pw
                user.password_hashed = hashed_pw
                user.password_salt = salt
                db.session.commit()
                
                response = jsonify({
                    'change-password-result' : 'succeeded'
                })
            else: response = jsonify({ #current pw unmatched
                'change-password-result': 'failed'
            })
        
    except Exception as e:
        print(str(e))
        return '', 500
    
    return response


@app.route('/users/login', methods=['POST'])
def login():
    entered_pw = request.json['password']
    email = request.json['email']
    try:
        user = User.query.filter_by(email=email).first()
        if(user): #if user with provided email exists
            valid = validate_pw(user, entered_pw)
            
            if(valid): #if password matched
                response = jsonify({
                    'user': user.serialize(),
                    'login-result': 'succeeded'
                })
            else:
                response = jsonify({ #if password unmatched
                    'login-result': 'failed'
                })
        else: 
            response = jsonify({ #if user with provided email doesnt exist
                'login-result': 'failed'
            })
        
    except Exception as e:
        print(str(e))
        return '', 500
    
    return response




@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()
        response = jsonify({
            'delete-result': 'succeeded'
        })
    except Exception as e:
        print(e)
        return '', 500
    
    return response

