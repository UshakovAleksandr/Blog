from api import db
from api.models.user import UserModel
from datetime import datetime


class NoteModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(300), unique=False, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey(UserModel.id))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # def __init__(self, user, note):
    #     self.user_id = user.id
    #     self.note = note

    # def to_dict(self):
    #     d = {}
    #     for column in self.__table__.columns:
    #         d[column.name] = str(getattr(self, column.name))
    #     return d
