from zoooop import db
from zoooop import admin
from flask import redirect, url_for, request
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_admin.contrib.sqla import ModelView 
from zoooop.models.User import *   
from zoooop.models.Blog import *  

    
class Blogs_Action(db.Model):
    action_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("Users.user_id"),nullable=False)
    post_id = db.Column(db.Integer,db.ForeignKey("Blogs.post_id"),nullable=False)
    likes = db.Column(db.Boolean, nullable=False,default=False)
    dislikes = db.Column(db.Boolean, nullable=False,default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    

    def __repr__(self) -> str:
        return f"{self.action_id}-{self.user_id}"
    
admin.add_view(ModelView(Blogs_Action,db.session))