from api import ma
from api.models.tag import TagModel
from api.schemas.user import UserResponseSchema


class TagRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TagModel

    name = ma.Str()


class TagResponseSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TagModel

    name = ma.auto_field()
    author = ma.Nested(UserResponseSchema)
