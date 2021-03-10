from api import app, api
from config import Config
from api.resources.note import NoteResource
from api.resources.user import UserResource
from api.resources.token import TokenResource


api.add_resource(UserResource, "/users", "/users/<int:user_id>")

api.add_resource(NoteResource, "/notes",
                               "/notes/<int:note_id>")

api.add_resource(TokenResource, "/auth/token")


if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
