from api import Resource, reqparse, db, abort
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

    ########################################################################################################
    #вариант 1
    # в данном варианте, как я и хочу, если нет юзера, то возвращается сообщение.
    # но нет обработки ошибок на случай ошибок с БД
    @marshal_with(UserResponseSchema)
    @doc(summary="Get user by id")
    def get(self, user_id):
        user = UserModel.query.get(user_id)
        if not user:
            abort(404, error=f"No user with id={user_id}")
        return user, 200

    # А данном варианте обработка ошибок на случай ошибок с БД происходит, но
    # тогда не возвращается сообщение про отстутвие юзера с указанием id, тк
    # думаю, что выбрасывается ошибка на еще когда user == None и до строки if not user код не доходит
    # и просто возвращается пустой словарь
    # вариант 2
    # @marshal_with(UserResponseSchema)
    # @doc(summary="Get user by id")
    # def get(self, user_id):
    #     try:
    #         user = UserModel.query.get(user_id)
    #         if not user:
    #             abort(404, error=f"No user with id={user_id}")
    #     except Exception as e:
    #         return {"error message": str(e)}, 400
    #     return user, 200


    # Как правильно сделать, и чтобы выбрасывались все исключения, которые я укажу и чтобы подстраховаться от ошибок БД
    # (отвалился коннект например или там еще много чего есть, насколько я прочитал)
    ########################################################################################################


    @use_kwargs(UserPutRequestSchema, location=('json'))
    @marshal_with(UserResponseSchema)
    @doc(summary="Change user by id")
    def put(self, user_id, **kwargs):
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
        users = UserModel.query.all()
        if not users:
            abort(404, error=f"No users yet")
        return users, 200

    @use_kwargs(UserRequestSchema, location=('json'))
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
