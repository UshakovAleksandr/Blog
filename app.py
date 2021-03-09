from api import app, api
from config import Config
from api.resources.note import NoteResource
from api.resources.user import UserResource


api.add_resource(UserResource, "/users", "/users/<int:user_id>")
api.add_resource(NoteResource, "/notes", "/users/<int:user_id>/notes",
                               "/users/<int:user_id>/notes/<int:note_id>")


if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
