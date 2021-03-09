from api import Resource, reqparse, db
from api.models.user import UserModel
from api.schemas.user import user_schema, users_schema


class UserResource(Resource):

    def get(self, user_id=None):
        if user_id is None:
            users = UserModel.query.all()
            if not users:
                return "There is no user yet", 200

        if user_id is not None:
            user = UserModel.query.get(user_id)
            if not user:
                return f"There is no user with id={user_id}", 404
            users = [user]

        #return [user.to_dict() for user in users], 200
        return users_schema.dump(users)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True)
        user_data = parser.parse_args()

        user = UserModel(**user_data)

        try:
            db.session.add(user)
            db.session.commit()
            #return user.to_dict(), 201
            return user_schema.dump(user)
        except:
            return "An error occurred while adding new user" \
                   "or an user with such name is already exist. " \
                    "You can only add a unique name", 404

    def put(self, user_id):
        user = UserModel.query.get(user_id)
        if not user:
            return f"No user with id={user_id}", 404
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        user_data = parser.parse_args()
        user.name = user_data["name"]
        try:
            db.session.add(user)
            db.session.commit()
            return user_schema.dump(user), 200
        except:
            return "An error occurred while changing the user", 404

    def delete(self, user_id):
        user = UserModel.query.get(user_id)
        if not user:
            return f"User with id={user_id} is not exists", 404

        try:
            db.session.delete(user)
            db.session.commit()
            return f"User with id={user_id} deleted", 200
        except:
            return "An error occurred while deleting the user", 404