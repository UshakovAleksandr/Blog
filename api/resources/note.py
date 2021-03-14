from api import Resource, reqparse, db, auth, abort, g
from api.models.note import NoteModel
from api.models.tag import TagModel
from api.schemas.note import NoteResponseSchema, NoteRequestSchema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from webargs import fields


@doc(tags=['Notes'], security=[{"basicAuth": []}])
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
    @use_kwargs(NoteRequestSchema, location='json')
    @marshal_with(NoteResponseSchema)
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
    def get(self):
        author = g.user
        notes = NoteModel.query.filter_by(author_id=author.id).all()
        if not notes:
            abort(404, error=f"You have no notes yet")
        return notes, 200

    @auth.login_required
    @use_kwargs(NoteRequestSchema, location='json')
    @marshal_with(NoteResponseSchema)
    def post(self, **kwargs):
        author = g.user
        note = NoteModel(author_id=author.id, **kwargs)
        note.save()
        return note, 201


@doc(tags=['Notes'])
class NotesPublicResource(MethodResource):

    @marshal_with(NoteResponseSchema(many=True))
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

    # @use_kwargs({"tags": fields.List(fields.Int())}, location=('json'))
    # def delete(self, note_id, **kwargs):
    #     note = NoteModel.query.get(1)
    #     print(note)
    #     print(note.tags)
    #     print(note.tags[0].id)
    #     print(note.tags[0].name)

        # if not note:
        #     abort(404, error=f"note {note_id} not found")
        # for tag_id in kwargs["tags"]:
        #db.session.remove()


@doc(tags=['Notes'])
class NoteFilterResource(MethodResource):

    @use_kwargs({"tag": fields.List(fields.Str())}, location='query')
    @marshal_with(NoteResponseSchema(many=True))
    def get(self, **kwargs):
        #print(kwargs)
        notes_lst = []
        for tag_id in kwargs["tag"]:
            """
            SELECT note FROM note_model
            LEFT JOIN tags
            ON  note_model.id = tags.note_model_id
            LEFT JOIN tag
            ON tags.tag_id = tag.id
            WHERE tag.name = "tag 2"
            """
            notes = db.session.query(NoteModel.note).\
                join(NoteModel.tags).filter(TagModel.name == tag_id).all()
            if not notes:
                abort(404, error=f"Notes with the specified tags were not found")
            for note in notes:
                if note not in notes_lst:
                    notes_lst.append(note)
        return notes_lst, 200
