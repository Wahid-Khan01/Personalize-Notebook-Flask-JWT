# from flask_restful import Resource
from flask import request, session, make_response, jsonify, Blueprint
from datetime import datetime, timedelta, timezone
from marshmallow import ValidationError
from hashlib import sha256
import jwt

from core.notes.models import Users
from core.notes.serde import users_schema
# from core import create_app

login = Blueprint("login", __name__) # create_app()
# class Login(Resource):
@login.route('/login', methods=['POST'])
def post():
    from core import x
    data = request.json
    try:
        va = users_schema().load(data)
    except ValidationError as e:
        return jsonify({'message':'Validation Error', 'errors':e}), 422
    user = Users.query.filter_by(email=va.get('email')).first()
    if user and user.password == sha256(va['password'].encode('utf-8')).hexdigest():
        session['uid'] = user.uid
        print("Session after login:", session)  # Debug print
        print("User's UID:", user.uid)
        payload = {'uid':user.uid, 'username': va['username'], 'email':va['email'], 'exp': datetime.now(timezone.utc) + timedelta(minutes=30)}
        token = jwt.encode(payload, x, algorithm='HS256')
        response = make_response(jsonify({'message':'login successful'}))
        response.set_cookie('token', token,httponly=True)
        return response
    else:
        return jsonify({'message':'invalid credentials'}), 401