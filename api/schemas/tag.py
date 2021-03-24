from api import ma
from api.models.tag import TagModel
from api.schemas.user import UserResponseSchema
from webargs import fields


class TagsSetRemoveNoteSchema(ma.SQLAlchemySchema):
    class Meta:
        pass
    """
    Валидационная схема входных данных привязки тега к заметке 
    """
    tags = fields.List(fields.Int())


class TagRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TagModel
    """
    Валидационная схема входных данных 
    """
    name = ma.Str()


class TagResponseSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TagModel
    """
    Валидационная схема выходных данных 
    """
    id = ma.auto_field()
    name = ma.auto_field()
    author = ma.Nested(UserResponseSchema)
