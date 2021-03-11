from api import Resource, reqparse, db, auth, abort, g
from api.models.note import NoteModel
from api.schemas.note import NoteResponseSchema, NoteRequestSchema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs


@doc(tags=['Notes'])
class NoteResource(MethodResource):

    @auth.login_required
    @marshal_with(NoteResponseSchema)
    def get(self, note_id):
        author = g.user
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"Note with id={note_id} not found")
        if note.author != author:
            abort(403, error=f"Access denied to note with id={note_id}")

        return note, 200

    @auth.login_required
    @use_kwargs(NoteRequestSchema, location=('json'))
    @marshal_with(NoteResponseSchema)
    def put(self, note_id, **kwargs):
        author = g.user
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"Note with id={note_id} not found")

        if note.author != author:
            abort(403, error=f"Access denied to note with id={note_id}")

        note.note = kwargs["note"]
        try:
            note.save()
            return note, 200
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
            note.delete()
            return f"Note with id={note_id} deleted", 200
        except:
            abort(404, error=f"An error occurred while changing note")


@doc(tags=['NotesList'])
class NoteListResource(MethodResource):

    @auth.login_required
    @marshal_with(NoteResponseSchema(many=True))
    def get(self):
        author = g.user
        notes = NoteModel.query.filter_by(author_id=author.id).all()
        if not notes:
            abort(404, error=f"You have no notes yet")
        return notes, 200

    @auth.login_required
    @use_kwargs(NoteRequestSchema, location=('json'))
    @marshal_with(NoteResponseSchema)
    def post(self, **kwargs):
        author = g.user
        note = NoteModel(author_id=author.id, **kwargs)
        note.save()
        return note, 201














