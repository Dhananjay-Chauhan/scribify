from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView  
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SECRET_KEY'] = "dingdingdingdingding"
db = SQLAlchemy(app)
admin = Admin(app)
from .routes import *
# with app.app_context():
#     db.create_all()