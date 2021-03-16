from api import Resource, reqparse, db, auth, abort, g
from api.models.note import NoteModel
from api.models.tag import TagModel
from api.schemas.note import NoteResponseSchema, NoteRequestSchema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from webargs import fields
import pdb


@doc(tags=['Notes'], security=[{"basicAuth": []}])
class NoteResource(MethodResource):

    @auth.login_required
    @marshal_with(NoteResponseSchema)
    @doc(summary="Get note by id")
    def get(self, note_id):
        author = g.user
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"Note with id={note_id} not found")
        if note.author != author:
            abort(403, error=f"Access denied to note with id={note_id}")

        return note, 200

    @auth.login_required
    @use_kwargs(NoteRequestSchema, location='json')
    @marshal_with(NoteResponseSchema)
    @doc(summary="Change note by id")
    def put(self, note_id, **kwargs):
        author = g.user
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"Note with id={note_id} not found")

        if note.author != author:
            abort(403, error=f"Access denied to note with id={note_id}")

        note.note = kwargs["note"]
        note.private = kwargs["private"]
        try:
            note.save()
            return note, 200
        except:
            abort(404, error=f"An error occurred while changing note")

    @auth.login_required
    @doc(summary="Delete note by id")
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


@doc(tags=['Notes'], security=[{"basicAuth": []}])
class NoteListResource(MethodResource):

    @auth.login_required
    @marshal_with(NoteResponseSchema(many=True))
    @doc(summary="Get all notes")
    def get(self):
        author = g.user
        notes = NoteModel.query.filter_by(author_id=author.id).all()
        if not notes:
            abort(404, error=f"You have no notes yet")
        return notes, 200

    @auth.login_required
    @use_kwargs(NoteRequestSchema, location='json')
    @marshal_with(NoteResponseSchema)
    @doc(summary="Create note")
    def post(self, **kwargs):
        author = g.user
        note = NoteModel(author_id=author.id, **kwargs)
        note.save()
        return note, 201


@doc(tags=['Notes'])
class NotesPublicResource(MethodResource):

    @marshal_with(NoteResponseSchema(many=True))
    @doc(summary="Get all public notes")
    def get(self):
        notes = NoteModel.query.filter_by(private=False).all()
        return notes, 200


@doc(tags=['Notes'])
class NoteSetTagsResource(MethodResource):
    @doc(summary="Set tags to Note")
    @use_kwargs({"tags": fields.List(fields.Int())}, location='json')
    @marshal_with(NoteResponseSchema)
    def put(self, note_id, **kwargs):
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"note with id={note_id} not found")
        for tag_id in kwargs["tags"]:
            tag = TagModel.query.get(tag_id)
            if not tag:
                abort(404, error=f"Tag with id={tag_id} not found")
            note.tags.append(tag)
        note.save()
        return note, 200

    @doc(summary="Delete tags from Note")
    @use_kwargs({"tags": fields.List(fields.Int())}, location='json')
    @marshal_with(NoteResponseSchema)
    def delete(self, note_id, **kwargs):
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"note with id={note_id} not found")
        for tag_id in kwargs["tags"]:
            tag = TagModel.query.get(tag_id)
            if not tag:
                abort(404, error=f"Tag with id={kwargs} not found")
            try:
                note.tags.remove(tag)
            except:
                abort(404, error=f"Note with id={note_id} have no tag with id={tag_id}")
        note.save()
        return note, 200


@doc(tags=['Notes'])
class NoteFilterResource(MethodResource):

    @use_kwargs({"tag": fields.List(fields.Str())}, location='query')
    @marshal_with(NoteResponseSchema(many=True))
    def get(self, **kwargs):
        notes_lst = []
        for tag_name in kwargs["tag"]:
            #pdb.set_trace()
            note = NoteModel.query.filter(NoteModel.tags.any(name=tag_name)).all()
            if not note:
                abort(404, error=f"Note with the specified tagname={tag_name} not found")
            if note[0] not in notes_lst:
                notes_lst.append(note[0])

        return notes_lst, 200
