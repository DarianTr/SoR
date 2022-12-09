from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_alembic import Alembic
from sqlalchemy import create_engine
import config
import pymysql

pymysql.install_as_MySQLdb()
engine = create_engine(config.database_url, echo=True)
engine.connect()

app = Flask(__name__)
app.config['ALEMBIC'] = {"version_locations": "../alembic"}
app.config['SECRET_KEY'] = config.secret_key
app.config['SQLALCHEMY_DATABASE_URI'] =  config.database_url
database = SQLAlchemy(app)

