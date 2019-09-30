import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

login_manager = LoginManager()
UPLOAD_FOLDER = 'uploads'


app = Flask(__name__)

app.config['SECRET_KEY']="sourcecode369"
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)
Migrate(app, db)
Bootstrap(app)

login_manager.init_app(app)
login_manager.login_view = 'login'

