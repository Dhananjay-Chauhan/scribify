from zoooop import db
from zoooop import admin
from flask import redirect, url_for, request
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_admin.contrib.sqla import ModelView 
# from .User import Users 
class Blogs(db.Model):
    __tablename__="Blogs"
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"),nullable=False)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    # user = db.relationship('Users',back_populates='posts')    

    def __repr__(self) -> str:
        return f"{self.post_id}-{self.slug}"
    

class ModelViewBlogs(ModelView) :
    form_columns = ['user_id', 'title','author','content','tags','slug','date_created'] 

admin.add_view(ModelViewBlogs(Blogs,db.session))