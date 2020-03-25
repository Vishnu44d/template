from flask import request, Blueprint, jsonify
from temp.models.userModel import User
from temp.models.menuModel import Meal
from temp.auth import get_token, validate_token, get_staff_token
import uuid
import datetime
import json
from pytz import timezone

userBP = Blueprint('userApi', __name__)

@userBP.route('/register', methods=['POST'])
def useraction():
    if request.method == 'POST':
        data = request.json
        print(data)
        return save_new_user(data=data)
    else:
        response_object = {
            'status': 'fail',
            'message': 'method not allowed',
        }
        return jsonify(response_object), 400


def save_new_user(data):
    from server import SQLSession
    session = SQLSession()
    # print(data)
    user = session.query(User).filter_by(email=data['email']).first()
    if not user:
        new_user = User(
            public_id=str(uuid.uuid4()),
            email=data['email'],
            username=data['name'],
            password=data['password'],
            registered_on=datetime.datetime.utcnow(),
            last_updated_on=datetime.datetime.utcnow()
        )
        try:
            session.add(new_user)
            session.commit()
            session.close()
            response_object = {
                'status': 'Ok',
                'message': 'User Created Successful',
            }
            return jsonify(response_object), 200
            
        except Exception as e:
            session.close()
            response_object = {
                'status': 'fail',
                'message': 'Problem saving in db',
                'error': str(e)
            }
            return jsonify(response_object), 500
    else:
        session.close()
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in. or try another email',
        }
        return jsonify(response_object), 400


@userBP.route('/login', methods=['POST'])
def login():
    data = request.json
    return get_token(data)


@userBP.route('/', methods=['POST'])
def get_my_detail():
    data = request.json
    valid_token, usr_ = validate_token(data)
    if valid_token:
        result = {
            "name": usr_.username,
            "email": usr_.email,
            "varified": usr_.varified,
            "admin":usr_.admin,
            "created_on":usr_.registered_on, 
            "last_update":usr_.last_updated_on
        }

        response_object = {
            'status': 'success',
            'message': 'detail of the user',
            'payload': result
        }
        return jsonify(response_object), 200

    else:
        response_object = {
            'status': 'fail',
            'message': 'invalid token',
        }
        return jsonify(response_object), 300

