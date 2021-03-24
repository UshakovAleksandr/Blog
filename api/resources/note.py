from api import Resource, reqparse, db, auth, abort, g
from api.models.note import NoteModel
from api.models.tag import TagModel
from api.schemas.note import NoteResponseSchema, NotePostRequestSchema,\
                             NotePutRequestSchema, NoteFilterSchema
from api.schemas.tag import TagsSetRemoveNoteSchema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
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
    @use_kwargs(NotePutRequestSchema, location='json')
    @marshal_with(NoteResponseSchema)
    @doc(summary="Change note by id")
    def put(self, note_id, **kwargs):
        author = g.user
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"Note with id={note_id} not found")
        if note.author != author:
            abort(403, error=f"Access denied to note with id={note_id}")
        for key in kwargs.keys():
            setattr(note, key, kwargs[key])
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
        notes = NoteModel.get_all_notes(author, archive="all")
        if not notes:
            abort(404, error=f"You have no notes yet")
        return notes, 200

    @auth.login_required
    @use_kwargs(NotePostRequestSchema, location='json')
    @marshal_with(NoteResponseSchema)
    @doc(summary="Create note")
    def post(self, **kwargs):
        author = g.user
        note = NoteModel(author_id=author.id, **kwargs)
        note.save()
        return note, 201


@doc(tags=['Notes'], security=[{"basicAuth": []}])
class NoteListNoArchiveResource(MethodResource):

    @auth.login_required
    @marshal_with(NoteResponseSchema(many=True))
    @doc(summary="Get all no_archive notes")
    def get(self):
        author = g.user
        notes = NoteModel.get_all_notes(author, archive="no_archive")
        if not notes:
            abort(404, error=f"You have no notes yet")
        return notes, 200


@doc(tags=['Notes'], security=[{"basicAuth": []}])
class NoteListArchiveResource(MethodResource):

    @auth.login_required
    @marshal_with(NoteResponseSchema(many=True))
    @doc(summary="Get all archive notes")
    def get(self):
        author = g.user
        notes = NoteModel.get_all_notes(author, archive="archive")
        if not notes:
            abort(404, error=f"You have no notes yet")
        return notes, 200


@doc(tags=['Notes'], security=[{"basicAuth": []}])
class NoteToArchiveResource(MethodResource):

    @auth.login_required
    @marshal_with(NoteResponseSchema)
    @doc(summary="Put note to archive")
    def put(self, note_id):
        author = g.user
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"Note with id={note_id} not found")
        if note.author != author:
            abort(403, error=f"Access denied to note with id={note_id}")
        note.archive = True
        note.save()
        return note, 200


@doc(tags=['Notes'], security=[{"basicAuth": []}])
class NoteRestoreResource(MethodResource):

    @auth.login_required
    @marshal_with(NoteResponseSchema)
    @doc(summary="Get note from archive")
    def put(self, note_id):
        author = g.user
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"Note with id={note_id} not found")
        if note.author != author:
            abort(403, error=f"Access denied to note with id={note_id}")
        note.archive = False
        note.save()
        return note, 200


@doc(tags=['Notes'])
class NotesPublicResource(MethodResource):

    @marshal_with(NoteResponseSchema(many=True))
    @doc(summary="Get all public notes")
    def get(self):
        notes = NoteModel.get_all_public_notes()
        if not notes:
            abort(404, error=f"Public notes not found")
        return notes, 200


@doc(tags=['Notes'], security=[{"basicAuth": []}])
class NoteSetTagsResource(MethodResource):

    @auth.login_required
    @doc(summary="Set tags to note")
    @use_kwargs(TagsSetRemoveNoteSchema, location='json')
    @marshal_with(NoteResponseSchema)
    def put(self, note_id, **kwargs):
        author = g.user
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"note with id={note_id} not found")
        if note.author != author:
            abort(403, error=f"Access denied to note with id={note_id}")
        for tag_id in kwargs["tags"]:
            tag = TagModel.query.get(tag_id)
            if not tag:
                abort(404, error=f"Tag with id={tag_id} not found")
            if tag.author != author:
                abort(403, error=f"Access denied to tag with id={tag_id}")
            note.tags.append(tag)
        note.save()
        return note, 200


@doc(tags=['Notes'], security=[{"basicAuth": []}])
class NoteRemoveTagsResource(MethodResource):

    @auth.login_required
    @doc(summary="Remove tags from note")
    @use_kwargs(TagsSetRemoveNoteSchema, location='json')
    @marshal_with(NoteResponseSchema)
    def put(self, note_id, **kwargs):
        author = g.user
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"note with id={note_id} not found")
        if note.author != author:
            abort(403, error=f"Access denied to note with id={note_id}")
        for tag_id in kwargs["tags"]:
            tag = TagModel.query.get(tag_id)
            if not tag:
                abort(404, error=f"Tag with id={tag_id} not found")
            if tag.author != author:
                abort(403, error=f"Access denied to tag with id={tag_id}")
            try:
                note.tags.remove(tag)
            except ValueError:
                abort(400, error=f"Note with id={note_id} has no tag with id={tag_id}")
            except:
                abort(404, error=f"An error occurred while removing tag from note."
                                 f" May be connection problems with DB. ")
        note.save()
        return note, 200


@doc(tags=['Notes'])
class NoteFilterResource(MethodResource):

    @doc(summary="Get notes. Filter by tags")
    @use_kwargs(NoteFilterSchema, location='query')
    @marshal_with(NoteResponseSchema(many=True))
    def get(self, **kwargs):
        notes_lst = []
        for tag_name in kwargs["tags"]:
            #pdb.set_trace()
            notes = NoteModel.get_notes_filtered_by_tags(tag_name)
            if not notes:
                abort(404, error=f"Note with tag_name={tag_name} not found")
            for note in notes:
                if note not in notes_lst:
                    notes_lst.append(note)
        return notes_lst, 200
