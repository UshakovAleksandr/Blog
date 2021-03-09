from api import db, datetime
from api.models.user import UserModel


class NoteModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    note = db.Column(db.String(300), unique=False)
    status = db.Column(db.String(10), unique=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey(UserModel.id))

    def __init__(self, user, title, note):
        self.user_id = user.id
        self.title = title
        self.note = note
        self.status = "private"

    # def to_dict(self):
    #     d = {}
    #     for column in self.__table__.columns:
    #         d[column.name] = str(getattr(self, column.name))
    #     return d
