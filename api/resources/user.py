from api import Resource, reqparse, db, abort
from api.models.user import UserModel
from api.schemas.user import UserRequestSchema, UserResponseSchema, user_schema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs


@doc(description='Api for notes.', tags=['Users'])
class UserResource(MethodResource):

    @marshal_with(UserResponseSchema)
    def get(self, user_id):
        user = UserModel.query.get(user_id)
        if not user:
            abort(404, error=f"No user with id={user_id}")
        return user, 200

    @use_kwargs(UserRequestSchema, location=('json'))
    @marshal_with(UserResponseSchema)
    def post(self, **kwargs):
        user = UserModel(**kwargs)
        try:
            user.save()
            return user, 201
        except:
            abort(404, error=f"An error occurred while adding new user"\
                              "or an user with such name is already exist. "\
                              "You can only add a unique name")

    def put(self, user_id):
        user = UserModel.query.get(user_id)
        if not user:
            abort(404, error=f"No user with id={user_id}")

        parser = reqparse.RequestParser()
        parser.add_argument("username")
        user_data = parser.parse_args()
        user.username = user_data["username"]
        try:
            user.save()
            return user_schema.dump(user), 200
        except:
            abort(404, error=f"An error occurred while changing the user")

    def delete(self, user_id):
        user = UserModel.query.get(user_id)
        if not user:
            abort(404, error=f"User with id={user_id} is not exists")
        try:
            db.session.delete(user)
            db.session.commit()
            return f"User with id={user_id} deleted", 200
        except:
            abort(404, error=f"An error occurred while deleting the user")


@doc(description='Api for notes.', tags=['UsersList'])
class UserListResource(MethodResource):

    @marshal_with(UserResponseSchema(many=True))
    def get(self):
        users = UserModel.query.all()
        if not users:
            abort(404, error=f"No users yet")
        return users, 200
