from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask.ext.login import LoginManager
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)

from app import view, model, form, controller