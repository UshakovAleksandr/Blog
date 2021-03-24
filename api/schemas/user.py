from api import ma
from api.models.user import UserModel


class UserRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel
    """
    Валидационная схема входных данных 
    """
    username = ma.Str()
    password = ma.Str()


class UserResponseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        """
        Валидационная схема выходных данных
        """
        model = UserModel
        fields = ("id", "username")


class UserPutRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel
    """
    Валидационная схема входных данных put-запроса
    """
    username = ma.Str()
