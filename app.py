from api import app, api, docs
from config import Config
from api.resources.note import NoteResource, NoteListResource, NotesPublicResource
from api.resources.user import UserResource, UserListResource
from api.resources.token import TokenResource


api.add_resource(UserListResource, "/users")               # GET, POST

api.add_resource(UserResource, "/users/<int:user_id>")     # GET, PUT, DELETE

api.add_resource(NoteListResource, "/notes")               # GET, POST

api.add_resource(NoteResource, "/notes/<int:note_id>")     # GET, PUT, DELETE

api.add_resource(NotesPublicResource, "/notes/public")     # GET

api.add_resource(TokenResource, "/auth/token")             # GET


docs.register(UserResource)
docs.register(UserListResource)
docs.register(NoteResource)
docs.register(NoteListResource)
docs.register(NotesPublicResource)


if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
