from api import ma
from api.models.note import NoteModel
from api.schemas.user import UserSchema


class NoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = NoteModel

    id = ma.auto_field()
    note = ma.auto_field()
    date = ma.auto_field()
    author = ma.Nested(UserSchema())


note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)
