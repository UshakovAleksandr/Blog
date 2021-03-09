from api import Resource, reqparse, db
from api.models.note import NoteModel
from api.models.user import UserModel
from api.schemas.note import note_schema, notes_schema


class NoteResource(Resource):

    def get(self, user_id=None, note_id=None):
        if user_id is None and note_id is None:
            notes = NoteModel.query.all()
            if not notes:
                return "There are no notes yet", 200

        if user_id is not None and note_id is None:
            notes = NoteModel.query.filter(NoteModel.user_id == user_id).all()

        if user_id is not None and note_id is not None:
            note = NoteModel.query.filter(NoteModel.user_id == user_id, NoteModel.id == note_id).all()
            if not note:
                return f"User with id={user_id} has no note with id={note_id} or user is not exists", 404
            notes = note

        #return [note.to_dict() for note in notes], 200
        return notes_schema.dump(notes), 200

    def post(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument("title", required=True)
        parser.add_argument("note", required=True)
        note_data = parser.parse_args()

        user = UserModel.query.get(user_id)
        if user:
            note = NoteModel(user, **note_data)
            print(note)
            try:
                db.session.add(note)
                db.session.commit()
                #return note.to_dict(), 201
                return note_schema.dump(note)
            except:
                return "An error occurred while adding new note", 404
        else:
            return f"User with id={user_id} is not exists", 404

    def put(self, user_id, note_id):
        note = NoteModel.query.filter(NoteModel.user_id == user_id, NoteModel.id == note_id).all()
        if not note:
            return f"This user has no quote with id={note_id}", 404
        parser = reqparse.RequestParser()
        parser.add_argument("title")
        parser.add_argument("note")
        note_data = parser.parse_args()

        note[0].title = note_data["title"] or note[0].title
        note[0].note = note_data["note"] or note[0].note

        try:
            db.session.add(note[0])
            db.session.commit()
            return note_schema.dump(note[0]), 200
        except:
            return "An error occurred while changing note", 404

    def delete(self, user_id, note_id):
        note = NoteModel.query.filter(NoteModel.user_id == user_id, NoteModel.id == note_id).all()
        print(note)
        if not note:
            return f"Note with id={note_id} is not exists", 404
        try:
            db.session.delete(note[0])
            db.session.commit()
            return f"Note with id={note_id} deleted", 200
        except:
            return "An error occurred while deleting the note", 404

