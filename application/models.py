from . import db
from datetime import datetime
from flask_login import UserMixin
from passlib.hash import sha256_crypt
from sqlalchemy import LargeBinary
from sqlalchemy import DDL

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    password = db.Column(LargeBinary, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    authentication = db.Column(db.Boolean, default=False)
    api_key = db.Column(db.String(255), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)


    def to_json(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin,
            'is_active': True 
        }
    
class UserAudit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    method = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer)
    old_username = db.Column(db.String(255))
    new_username = db.Column(db.String(255))
    old_email = db.Column(db.String(255))
    new_email = db.Column(db.String(255))
    old_first_name = db.Column(db.String(255))
    new_first_name = db.Column(db.String(255))
    old_last_name = db.Column(db.String(255))
    new_last_name = db.Column(db.String(255))
    log_time = db.Column(db.TIMESTAMP, default=datetime.utcnow)

   
