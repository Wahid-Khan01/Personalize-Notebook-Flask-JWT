# from flask_restful import Resource
from flask import request, Blueprint
from marshmallow import ValidationError
from hashlib import sha256

from core.notes.models import Users
from core.notes.serde import users_schema
from core import db

signup = Blueprint('signup', __name__) # create_app()

# class Signup(Resource):
@signup.route('/signup', methods=['POST'])
def post():
    data = request.json
    try:
        va = users_schema().dump(data)
    except ValidationError as e:
        return ({'message': 'Validation Error', 'Errors':e})
    
    existing_username = Users.query.filter_by(username=data["username"]).count()
    existing_email = Users.query.filter_by(email=data["email"]).count()
    
    if existing_username:
        return ({"message": "Username is already in use."}), 409

    if existing_email:
        return ({"message": "Email is already in use."}), 409

    if len(data["username"]) < 3:
        return ({"message":"username must be greater than 2 character."}), 422
    
    if len(data['password']) < 6:
        return {'message': 'password must be greater than 6 characters'}, 422
    
    p = sha256(data['password'].encode('utf-8')).hexdigest()
    
    signup = Users(username=data['username'], email=data['email'], password=p)
    db.session.add(signup)
    db.session.commit()
    return {'message':'sign up was successful'}, 200