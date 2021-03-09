from api import db


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    notes = db.relationship('NoteModel', backref='user', lazy='joined', cascade="all, delete-orphan")

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = str(getattr(self, column.name))
        return d
