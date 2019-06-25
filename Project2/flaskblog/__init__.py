from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ec14e62f6d91f3231b5b99bcd7d61836'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)    # this is a database sqlalchemy instance
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from flaskblog import routes
