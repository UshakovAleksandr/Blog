from api import Resource, reqparse, db, auth, abort, g
from api.models.note import NoteModel
from api.schemas.note import note_schema, notes_schema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs


class NoteResource(MethodResource):

    @auth.login_required
    def get(self, note_id=None):
        author = g.user
        if note_id is None:
            notes = NoteModel.query.filter_by(author_id=author.id).all()
            if not notes:
                abort(404, error=f"You have no notes yet")
            return notes_schema.dump(notes), 200

        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"Note with id={note_id} not found")
        if note.author != author:
            abort(403, error=f"Access denied to note with id={note_id}")

        return note_schema.dump(note), 200

    @auth.login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("note", required=True)
        note_data = parser.parse_args()
        author = g.user
        note = NoteModel(author_id=author.id, **note_data)
        db.session.add(note)
        db.session.commit()
        return note_schema.dump(note)

    @auth.login_required
    def put(self, note_id):
        note_parser = reqparse.RequestParser()
        note_parser.add_argument("note", required=True)
        note_data = note_parser.parse_args()
        author = g.user
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"Note with id={note_id} not found")

        if note.author != author:
            abort(403, error=f"Access denied to note with id={note_id}")

        note.note = note_data["note"]
        try:
            db.session.add(note)
            db.session.commit()
            return note_schema.dump(note), 200
        except:
            abort(404, error=f"An error occurred while changing note")

    @auth.login_required
    def delete(self, note_id):
        author = g.user
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"Note with id={note_id} not found")

        if note.author != author:
            abort(403, error=f"Access denied to note with id={note_id}")

        try:
            db.session.delete(note)
            db.session.commit()
            return f"Note with id={note_id} deleted", 200
        except:
            abort(404, error=f"An error occurred while changing note")
