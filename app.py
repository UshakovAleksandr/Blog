from api import app, api, docs
from config import Config
from api.resources.note import NoteResource
from api.resources.user import UserResource, UserListResource
from api.resources.token import TokenResource


api.add_resource(UserListResource, "/users")               # GET

api.add_resource(UserResource, "/users",                   # POST
                               "/users/<int:user_id>")     # GET, PUT, DELETE

api.add_resource(NoteResource, "/notes",
                               "/notes/<int:note_id>")

api.add_resource(TokenResource, "/auth/token")             # GET


docs.register(UserResource)
docs.register(UserListResource)
docs.register(NoteResource)


if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
