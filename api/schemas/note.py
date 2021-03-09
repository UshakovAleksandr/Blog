from api import ma
from api.models.note import NoteModel
from api.schemas.user import UserSchema


class NoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = NoteModel

    #fields = ("id", "username", "role")
    id = ma.auto_field()
    title = ma.auto_field()
    note = ma.auto_field()
    date = ma.auto_field()
    user = ma.Nested(UserSchema())


note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)
