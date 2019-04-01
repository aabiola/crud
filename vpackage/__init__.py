# pylint: disable-msg=C0103
'''This is the init file'''
# 3rd party imports
from flask import Flask

from flask_wtf.csrf import CSRFProtect

from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager

#import mysql.connector

#local imports
from vpackage.config import DevelopmentConfig


from flask_mail import Mail, Message

from flask_migrate import Migrate


app = Flask(__name__, instance_relative_config=True)

#load the config

app.config.from_object(DevelopmentConfig)
app.config.from_pyfile('config.py', silent=False)
app.config['UPLOAD_FOLDER'] = 'uploads/'


#config for mail

app.config['MAIL_SERVER'] = 'moatconsulting.com.ng'
app.config['MAIL_PORT'] = 465
#app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'bootcamp@moatconsulting.com.ng'  # enter your email here
app.config['MAIL_DEFAULT_SENDER'] = 'bootcamp@moatconsulting.com.ng' # enter your email here
app.config['MAIL_PASSWORD'] = 'moatserve2019' # enter your password here
app.config['MAIL_USE_SSL'] = True
#end config mail
db = SQLAlchemy(app)

csrf = CSRFProtect()
csrf.init_app(app)

migrate = Migrate(app, db)


login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_message = "You must be logged in to access this page."
#login_manager.login_view = "auth.login"


mail = Mail(app)


#load the views
from .views import allviews, api

