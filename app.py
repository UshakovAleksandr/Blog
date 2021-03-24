from api import app, api, docs
from config import Config
from api.resources.note import NoteResource, NoteListResource,\
                               NotesPublicResource, NoteSetTagsResource,\
                               NoteFilterResource, NoteRemoveTagsResource,\
                               NoteToArchiveResource, NoteRestoreResource,\
                               NoteListArchiveResource, NoteListNoArchiveResource
from api.resources.user import UserResource, UserListResource
from api.resources.tag import TagListResource, TagResource
from api.resources.token import TokenResource
from flask import render_template


@app.route("/", methods=["GET"])
def main_page():
    """
    Главная страница, ссылка на swagger
    """
    return render_template("index.html")


api.add_resource(UserListResource, "/users")               # GET, POST

api.add_resource(NoteListArchiveResource, "/notes/archive")  # GET

api.add_resource(NoteListNoArchiveResource, "/notes/no_archive")  # GET

api.add_resource(UserResource, "/users/<int:user_id>")     # GET, PUT, DELETE

api.add_resource(NoteListResource, "/notes")               # GET, POST

api.add_resource(NoteResource, "/notes/<int:note_id>")     # GET, PUT, DELETE

api.add_resource(NoteToArchiveResource, "/notes/<int:note_id>/to_archive")      # PUT

api.add_resource(NoteRestoreResource, "/notes/<int:note_id>/restore")      # PUT

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
docs.register(NoteToArchiveResource)
docs.register(NoteRestoreResource)
docs.register(NoteListArchiveResource)
docs.register(NoteListNoArchiveResource)
#docs.register(TokenResource)


if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
