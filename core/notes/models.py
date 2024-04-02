from core import db
from datetime import datetime, timezone


class Users(db.Model):
    __tablename__ = 'user'
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    notes = db.relationship('Notes')



class Notes(db.Model):
    __tablename__ = 'note'
    nid = db.Column(db.Integer, primary_key= True)
    data = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone.utc))
    userid = db.Column(db.Integer, db.ForeignKey("user.uid"))