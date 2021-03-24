from api import Resource, g, auth


class TokenResource(Resource):
    @auth.login_required
    def get(self):
        """
        Проверяется есть ли пользователь с тами Username и Password в БД
        и к нему создается токен через метод def generate_auth_token()
        :return: токен
        """
        token = g.user.generate_auth_token()
        return {'token': token.decode('ascii')}
