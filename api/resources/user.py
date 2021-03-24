from api import abort
from api.models.user import UserModel
from api.schemas.user import UserRequestSchema, UserResponseSchema, UserPutRequestSchema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs


@doc(tags=['Users'])
class UserResource(MethodResource):

    # @doc(
    #     summary="Get user by id",
    #     description="Returns user",
    #     produces=[
    #         'application/json'
    #     ],
    #     params={'user_id': {'description': 'user id'}},
    #     responses={
    #         "200": {
    #
    #             "description": "Return user",
    #             "content":
    #                 {"application/json": []}
    #
    #         },
    #         "404": {
    #             "description": "User not found"
    #         }
    #     }
    # )
    @marshal_with(UserResponseSchema)
    @doc(summary="Get user by id")
    def get(self, user_id):
        """
        Возвращает пользователя по id.
        :param user_id: id пользователя
        :return: пользователя
        """
        user = UserModel.query.get(user_id)
        if not user:
            abort(404, error=f"No user with id={user_id}")
        return user, 200

    @use_kwargs(UserPutRequestSchema, location='json')
    @marshal_with(UserResponseSchema)
    @doc(summary="Change user by id")
    def put(self, user_id, **kwargs):
        """
        Изменяет пользователя по id.
        :param user_id: id пользователя
        :param kwargs: параметры для изменения пользователя
        :return: пользователя
        """
        user = UserModel.query.get(user_id)
        if not user:
            abort(404, error=f"No user with id={user_id}")
        user.username = kwargs["username"]
        try:
            user.save()
            return user, 200
        except:
            abort(404, error=f"An error occurred while changing the user")

    @doc(summary="Delete user by id")
    def delete(self, user_id):
        """
        Удаляет пользователя по id.
        :param user_id: id пользователя
        :return: пользователя
        """
        user = UserModel.query.get(user_id)
        if not user:
            abort(404, error=f"User with id={user_id} is not exists")
        try:
            user.delete()
            return f"User with id={user_id} deleted", 200
        except:
            abort(404, error=f"An error occurred while deleting the user")


@doc(tags=['Users'])
class UserListResource(MethodResource):

    @marshal_with(UserResponseSchema(many=True))
    @doc(summary="Get all users")
    def get(self):
        """
        Возвращает всех пользователей
        :return: пользователи
        """
        users = UserModel.query.all()
        if not users:
            abort(404, error=f"No users yet")
        return users, 200

    @use_kwargs(UserRequestSchema, location='json')
    @marshal_with(UserResponseSchema)
    @doc(summary="Create new user")
    def post(self, **kwargs):
        user = UserModel(**kwargs)
        try:
            user.save()
            return user, 201
        except:
            abort(404, error=f"An error occurred while adding new user" \
                             "or a user with such name is already exist. " \
                             "You can only add a unique name")
