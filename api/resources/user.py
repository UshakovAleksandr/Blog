from api import Resource, reqparse, db, abort
from api.models.user import UserModel
from api.schemas.user import user_schema, users_schema


class UserResource(Resource):

    def get(self, user_id=None):
        if user_id is None:
            users = UserModel.query.all()
            if not users:
                abort(404, error=f"No users yet")

        if user_id is not None:
            user = UserModel.query.get(user_id)
            if not user:
                abort(404, error=f"No user with id={user_id}")
            users = [user]

        return users_schema.dump(users)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True)
        parser.add_argument("password", required=True)
        user_data = parser.parse_args()

        user = UserModel(**user_data)

        try:
            user.save()
            return user_schema.dump(user), 201
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
