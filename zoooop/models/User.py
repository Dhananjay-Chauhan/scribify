# import app    
from zoooop import db
from zoooop import admin
from flask import redirect, url_for, request
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_admin.contrib.sqla import ModelView  
from flask_login import UserMixin
# db = SQLAlchemy()
class Users(db.Model,UserMixin):
    __tablename__="Users"
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    # posts = db.relationship('Blogs',back_populates='user')   
    def __repr__(self) -> str:
        return f"{self.user_id}-{self.name}"
    
    def get_id(self):
       return self.user_id

class ModelViewUsers(ModelView) :
    form_columns = ['user_id', 'name','email','password','username','phone_number','date_created'] 
admin.add_view(ModelViewUsers(Users,db.session))