from flask import request, jsonify
from temp.models.userModel import User
import jwt
import os
import datetime
from dotenv import load_dotenv

load_dotenv()

def validate_token(data):
    '''
    Return bollean 
    true -> valid token.... 
    false -> Invalid token....
    takes dict as input having field "token"
    '''
    token = data['token']
    try:
        from server import SQLSession
        session = SQLSession()
        d = jwt.decode(token, os.environ.get('SECRET_KEY'))
        usr = d['email']

        user_ = session.query(User).filter_by(email=usr).first()
        session.close()
        if not user_:
            return False, None
        else:
            return True, user_
    except:
        return False, None

def validate_admin(data):
    res = validate_token(data)
    if(res[0]):
        return res[1].admin
    else:
        return False


def get_token(data):
    from server import SQLSession
    session = SQLSession()
    user = session.query(User).filter_by(email=data['email']).first()
    session.close()
    if not user:
        responce_object = {
            'Status': 'fail',
            'message': 'no such user exist',
        }
        return jsonify(responce_object), 400
    else:
        if user.check_password(data.get('password')):
            if user.varified:
                responce_object = {
                    'status': 'success',
                    'message': 'Given the token. Use it wisely',
                    'token': jwt.encode({'email': user.email, 'exp':datetime.datetime.utcnow() + datetime.timedelta(days=90)}, os.environ.get('SECRET_KEY')).decode('UTF-8'),
                    'email': data['email']
                }
                return jsonify(responce_object), 200
            else:
                responce_object = {
                    'status': 'fail',
                    'message': 'Not varified yet',
                }
                return jsonify(responce_object), 400
        else:
            responce_object = {
                'status': 'fail',
                'message': 'enter valid password/email'
            }
            return jsonify(responce_object), 400

