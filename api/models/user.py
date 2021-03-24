from api import db, Config
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                         as Serializer, BadSignature, SignatureExpired)


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(128))
    notes = db.relationship('NoteModel', backref='author', lazy='joined', cascade="all, delete-orphan")
    tags = db.relationship('TagModel', backref='author', lazy='joined', cascade="all, delete-orphan")

    def __init__(self, username, password):
        self.username = username
        self.hash_password(password)

    def hash_password(self, password):
        """
        Хэширует пароль пользователья при регистрации
        :param password: пароль пользователя из конструктора
        """
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        """
        Проверяет корректность пароля при аутентификаци
        :param password: пароль пользователя
        :return: bool
        """
        return pwd_context.verify(password, self.password_hash)

    # 1.2 создает токен, вызывается в русурсе "токен"
    def generate_auth_token(self, expiration=600):
        """
        Создает токен
        """
        s = Serializer(Config.SECRET_KEY, expires_in=expiration)
        return s.dumps({'id': self.id})

    def save(self):
        """
        Сохраняет пользователя в БД
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Удаляет пользователя из БД
        """
        db.session.delete(self)
        db.session.commit()

    # 2.2 проверяет валидность пришедшего токена. Вызывается из init
    @staticmethod
    def verify_auth_token(token):
        """
        Проверяет валидность пришедшего токена
        """
        s = Serializer(Config.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = UserModel.query.get(data['id'])
        return user
