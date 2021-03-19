from api import ma
from api.models.note import NoteModel
from api.schemas.user import UserResponseSchema
from api.schemas.tag import TagResponseSchema


class NotePostRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = NoteModel

    note = ma.Str()
    private = ma.Bool(required=False)


class NotePutRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = NoteModel

    note = ma.Str(required=False)
    private = ma.Bool(required=False)


class NoteResponseSchema(ma.SQLAlchemySchema):
    class Meta:
        model = NoteModel

    id = ma.auto_field()
    note = ma.auto_field()
    private = ma.auto_field()
    date = ma.auto_field()
    archive = ma.auto_field()
    author = ma.Nested(UserResponseSchema())
    tags = ma.Nested(TagResponseSchema(many=True))
