from api import Resource, g, auth


# 1.1 проверяется есть ли пользователь с тами Username и Password в БД
# и к нему создается токен через метод def generate_auth_token()
class TokenResource(Resource):
    @auth.login_required
    def get(self):
        token = g.user.generate_auth_token()
        return {'token': token.decode('ascii')}
