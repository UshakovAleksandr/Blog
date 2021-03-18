from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from api.schemas.tag import TagRequestSchema, TagResponseSchema
from api.models.tag import TagModel
from api import abort, auth, g


@doc(tags=['Tags'], security=[{"basicAuth": []}])
class TagResource(MethodResource):

    @auth.login_required
    @doc(summary="Get tag by id")
    @marshal_with(TagResponseSchema)
    def get(self, tag_id):
        author = g.user
        tag = TagModel.query.get(tag_id)
        if not tag:
            abort(404, error=f"Tag with id={tag_id} not found")
        if tag.author != author:
            abort(403, error=f"Access denied to tag with id={tag_id}")
        return tag, 200

    @auth.login_required
    @doc(summary="Change tag by id")
    @use_kwargs(TagRequestSchema, location='json')
    @marshal_with(TagResponseSchema)
    def put(self, tag_id, **kwargs):
        author = g.user
        tag = TagModel.query.get(tag_id)
        if not tag:
            abort(404, error=f"Tag with id={tag_id} not found")
        if tag.author != author:
            abort(403, error=f"Access denied to tag with id={tag_id}")
        tag.name = kwargs["name"]
        try:
            tag.save()
            return tag, 200
        except:
            abort(404, error=f"An error occurred while changing tag"
                             f" or a tag with such name is already exist.")

    @auth.login_required
    @doc(summary="Delete tag by id")
    def delete(self, tag_id):
        author = g.user
        tag = TagModel.query.get(tag_id)
        if not tag:
            abort(404, error=f"Tag with id={tag_id} not found")
        if tag.author != author:
            abort(403, error=f"Access denied to tag with id={tag_id}")
        try:
            tag.delete()
            return f"Tag with id={tag_id} deleted", 200
        except:
            abort(404, error=f"An error occurred while changing note")


@doc(tags=['Tags'], security=[{"basicAuth": []}])
class TagListResource(MethodResource):

    @auth.login_required
    @doc(summary="Get all tags")
    @marshal_with(TagResponseSchema(many=True))
    def get(self):
        author = g.user
        tags = TagModel.query.filter_by(author_id=author.id).all()
        if not tags:
            abort(404, error=f"No tags yet")
        return tags, 200

    @auth.login_required
    @doc(summary="Create new tag")
    @use_kwargs(TagRequestSchema, location='json')
    @marshal_with(TagResponseSchema)
    def post(self, **kwargs):
        author = g.user
        tag = TagModel(author_id=author.id, **kwargs)
        try:
            tag.save()
            return tag, 201
        except:
            abort(404, error=f"An error occurred while adding new tag"
                             " or a tag with such name is already exist. "
                             "You can only add a unique tag")
