import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Jamandalley'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://root:@localhost/recobank_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
