from api import ma
from api.models.user import UserModel


class UserRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel

    username = ma.Str()
    password = ma.Str()


class UserResponseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        fields = ("id", "username")


class UserRequestPutSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel

    username = ma.Str()
