#import logging
from flask import Flask, g
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_marshmallow import Marshmallow
from flask_httpauth import HTTPBasicAuth
from flask_apispec.extension import FlaskApiSpec


app = Flask(__name__)
app.config.from_object(Config)

# logging.basicConfig(filename='record.log',
#                    level=logging.INFO,
#                    format=f'%(asctime)s %(levelname)s %(name)s : %(message)s')
# # Настройка уровня логирования flask
# app.logger.setLevel(logging.INFO)
# # Настройка уровня логирования сервера-разработки werkzeug
# logging.getLogger('werkzeug').setLevel(logging.INFO)

api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
ma = Marshmallow(app)
auth = HTTPBasicAuth()
docs = FlaskApiSpec(app)

client = app.test_client()

# 2.1 проверка данных из запроса
# Проверяет или username, password или token
@auth.verify_password
def verify_password(username_or_token, password):
    from api.models.user import UserModel
    #print("username_or_token = ", username_or_token)
    user = UserModel.verify_auth_token(username_or_token)
    if not user:
        user = UserModel.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True
