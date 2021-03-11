from api import ma
from api.models.note import NoteModel
from api.schemas.user import UserResponseSchema


class NoteRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = NoteModel

    note = ma.Str()


class NoteResponseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = NoteModel

    id = ma.auto_field()
    note = ma.auto_field()
    date = ma.auto_field()
    author = ma.Nested(UserResponseSchema())

