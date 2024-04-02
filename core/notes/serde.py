from marshmallow import Schema, fields

class users_schema(Schema):
    uid = fields.Int()
    username = fields.Str()
    email = fields.Str()
    password = fields.Str()

class notes_schema(Schema):
    nid = fields.Int()
    data = fields.Str()
    date = fields.DateTime()
    userid = fields.Int()
