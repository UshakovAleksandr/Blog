from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from api.schemas.tag import TagRequestSchema, TagResponseSchema
from api.models.tag import TagModel
from api import abort


@doc(tags=['Tags'])
class TagResource(MethodResource):

    @doc(summary="Get tag by id")
    @marshal_with(TagResponseSchema)
    def get(self, tag_id):
        tag = TagModel.query.get(tag_id)
        if not tag:
            abort(404, error=f"Tag with id={tag_id} not found")
        return tag, 200

    @doc(summary="Change tag by id")
    @use_kwargs(TagRequestSchema, location='json')
    @marshal_with(TagResponseSchema)
    def put(self, tag_id, **kwargs):
        tag = TagModel.query.get(tag_id)
        if not tag:
            abort(404, error=f"Tag with id={tag_id} not found")
        tag.name = kwargs["name"]
        try:
            tag.save()
            return tag, 200
        except:
            abort(404, error=f"An error occurred while changing tag")

    @doc(summary="Delete tag by id")
    def delete(self, tag_id):
        tag = TagModel.query.get(tag_id)
        if not tag:
            abort(404, error=f"Tag with id={tag_id} not found")
        try:
            tag.delete()
            return f"Tag with id={tag_id} deleted"
        except:
            abort(404, error=f"An error occurred while changing note")


@doc(tags=['Tags'])
class TagListResource(MethodResource):

    @doc(summary="Get all tags")
    @marshal_with(TagResponseSchema(many=True))
    def get(self):
        tags = TagModel.query.all()
        if not tags:
            abort(404, error=f"No tags yet")
        return tags, 200

    @doc(summary="Create new tag")
    @use_kwargs(TagRequestSchema, location='json')
    @marshal_with(TagResponseSchema)
    def post(self, **kwargs):
        tag = TagModel(**kwargs)
        try:
            tag.save()
            return tag, 201
        except:
            abort(404, error=f"An error occurred while adding new tag" \
                             "or a tag with such name is already exist. " \
                             "You can only add a unique tag")
