# from website import app, database
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_alembic import Alembic
from sqlalchemy import create_engine
import config
import pymysql
from flask_login import LoginManager
import os

pymysql.install_as_MySQLdb()
engine = create_engine(config.database_url, echo=True, pool_pre_pring=True)
engine.connect()



app = Flask(__name__)
app.config['ALEMBIC'] = {"version_locations": "../alembic"}
app.config['SECRET_KEY'] = config.secret_key
app.config['SQLALCHEMY_DATABASE_URI'] =  config.database_url
database = SQLAlchemy(app)
    
def create_app():
    
    
    from .auth import auth 
    from .lehrer import lehrer 
    from .schueler import schueler
    from structure import Person
    
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(lehrer, url_prefix='/')
    app.register_blueprint(schueler, url_prefix='/')
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return Person.query.get(id)
    return app