from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_migrate import Migrate

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
CSRFProtect(app)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
Migrate(app, db)

from app import routes, models
