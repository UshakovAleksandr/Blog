from api import ma
from api.models.tag import TagModel


class TagRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TagModel

    name = ma.Str()


class TagResponseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TagModel
        fields = ("name", )
