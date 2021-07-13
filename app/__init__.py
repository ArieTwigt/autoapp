from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from flask_login import LoginManager

import sys

##### Configurations
load_dotenv()

app = Flask(__name__)

app.config.from_object(Config)
app.secret_key = os.environ.get('SECRET_KEY')

# Login
login = LoginManager(app)
login.login_view = 'login'

# Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models