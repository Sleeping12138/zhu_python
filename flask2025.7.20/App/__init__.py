from flask import Flask
from App.route.dressing import bp
from .exts import init_exts
from App.route.class_student import cs
from App.route.user_movie import um
from App.route.cache_test import ct
from App.Api.urls import *


def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)
    app.register_blueprint(cs)
    app.register_blueprint(um)
    app.register_blueprint(ct)

    db_url = 'mysql+pymysql://root:woshizjy12138@localhost:3306/flaskdb'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    init_exts(app=app)

    return app
