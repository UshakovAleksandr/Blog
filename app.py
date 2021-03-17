from api import app, api, docs
from config import Config
from api.resources.note import NoteResource, NoteListResource,\
                               NotesPublicResource, NoteSetTagsResource,\
                               NoteFilterResource, NoteRemoveTagsResource
from api.resources.user import UserResource, UserListResource
from api.resources.tag import TagListResource, TagResource
from api.resources.token import TokenResource


api.add_resource(UserListResource, "/users")               # GET, POST

api.add_resource(UserResource, "/users/<int:user_id>")     # GET, PUT, DELETE

api.add_resource(NoteListResource, "/notes")               # GET, POST

api.add_resource(NoteResource, "/notes/<int:note_id>")     # GET, PUT, DELETE

api.add_resource(NotesPublicResource, "/notes/public")     # GET

api.add_resource(TokenResource, "/auth/token")             # GET

api.add_resource(TagListResource, "/tags")                 # GET, POST

api.add_resource(TagResource, "/tags/<int:tag_id>")        # GET

api.add_resource(NoteSetTagsResource, "/notes/<int:note_id>/tags/set")  # PUT

api.add_resource(NoteRemoveTagsResource, "/notes/<int:note_id>/tags/remove")  # PUT

api.add_resource(NoteFilterResource, "/notes/filter")     # GET


docs.register(UserResource)
docs.register(UserListResource)
docs.register(NoteResource)
docs.register(NoteListResource)
docs.register(NotesPublicResource)
docs.register(TagListResource)
docs.register(TagResource)
docs.register(NoteSetTagsResource)
docs.register(NoteRemoveTagsResource)
docs.register(NoteFilterResource)


if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
