from flask import Flask, g
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_marshmallow import Marshmallow
from flask_httpauth import HTTPBasicAuth
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec


app = Flask(__name__)
app.config.from_object(Config)
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Notes Project',
        version='v1',
        plugins=[MarshmallowPlugin()], # генерация доков из схем в swagger
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger', # URI API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui'# URI UI of API Doc
})
api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
ma = Marshmallow(app)
auth = HTTPBasicAuth()
docs = FlaskApiSpec(app)


# 2.1 проверка данных из запроса
# Проверяет или username, password или token
@auth.verify_password
def verify_password(username_or_token, password):
    from api.models.user import UserModel
    # сначала проверяем authentication token
    print("username_or_token = ", username_or_token)
    user = UserModel.verify_auth_token(username_or_token)
    if not user:
        # потом авторизация
        user = UserModel.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True
