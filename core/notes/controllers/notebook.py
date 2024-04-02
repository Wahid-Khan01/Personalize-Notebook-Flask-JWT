# from flask_restful import Resource
from flask import request, session, jsonify, Blueprint
from marshmallow import ValidationError

from core.notes.serde import  notes_schema
from core.notes.models import Notes
from core.Authorization.decorators.auth_req import token_required
from core import db

foo = Blueprint("foo", __name__)
# class foo(Resource):
@foo.route('/view', methods=['GET'])
@token_required
def get():
    # note = Notes.query.filter_by().first()
    
    try:
        if records := Notes.query.filter_by(userid=session['uid']):
            valid = notes_schema().dump(records, many=True)
        else:
            return jsonify({'message':'No records found'}), 404
    except ValidationError as error:
        return jsonify({'message':'ValidationError', 'Error':error}), 400
    return jsonify(valid), 200
    
    # if not (data := notes_schema().dump(note, many=True)):
    #     return jsonify({'message':'no records found'}), 204
    # return jsonify(data), 200

@foo.route('/add', methods=['POST'])
@token_required
def post():
    if not (note := request.get_json()):
        return jsonify({'message': 'no data '}), 204
    print(note)
    
    try:
        va = notes_schema().load(note)
    except ValidationError as e:
        return jsonify({'message': 'Validation Error', 'errors': e.messages}), 422
    add_note = Notes(data=note['data'], userid=session['uid'])
    db.session.add(add_note)
    db.session.commit()
    return jsonify({'message': 'notes added'}), 200

@foo.route('/delete', methods=['DELETE'])
@token_required
def delete():
    if not (data:=request.get_json()):
        return ({'message':'no data provided'}), 204
    Notes().query.filter_by(nid=data['nid']).delete()
    db.session.commit()
    return jsonify({'message': f"{data['nid']} was successfully deleted"}), 200

@foo.route('/update', methods=['PUT'])
@token_required
def put():
    if not (data:=request.get_json()):
        return jsonify({'message':'no data provided'}), 204
    try:
        va = notes_schema().load(data)
    except ValidationError as e:
        return jsonify({'message':'Validation Error', 'errors': e}), 422
    except Exception as e:
        return jsonify({'error':e})
    
    Notes.query.filter_by(nid=data["nid"]).update(data,synchronize_session=False)
    db.session.commit()
    return jsonify({"message":"note is updated"})