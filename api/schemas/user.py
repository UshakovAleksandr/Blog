from api import ma
from api.models.user import UserModel


# Десериализация запроса на сервер
class UserRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel

    username = ma.Str()
    password = ma.Str()


# Сериализация ответа клиенту
class UserResponseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        fields = ("id", "username")


user_schema = UserResponseSchema()
users_schema = UserResponseSchema(many=True)
