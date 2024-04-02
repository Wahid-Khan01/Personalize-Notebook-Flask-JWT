# from flask_restful import Resource
from flask import session, request, jsonify, Blueprint
from marshmallow import ValidationError

from core.notes.models import Users
from core.notes.serde import users_schema
# from core import create_app

logout = Blueprint('logout', __name__) # create_app()

# class Logout(Resource):
@logout.route('/logout', methods=['POST'])
def post():
    data = request.json #email
    try:
        va = users_schema().load(data)
    except ValidationError as e:
        return jsonify({'message':'Validation Error', 'Errors': e}), 422

    user = Users.query.filter_by(email=data['email']).first()
    print("User:", user)               
    print("User's UID:", user.uid)     
    print("Session:", session)         
    print("Session's UID:", session.get('uid'))
    if not user or session.get('uid') != user.uid:
        return jsonify({'message': 'You need to login first'}), 401
    session.pop('uid')
    return jsonify({'message': 'logout was successful'}), 200
