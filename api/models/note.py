from api import db
from api.models.user import UserModel
from api.models.tag import TagModel
from datetime import datetime

tags = db.Table('tags',
                    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
                    db.Column('note_model_id', db.Integer, db.ForeignKey('note_model.id'), primary_key=True)
                    )


class NoteModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(300), unique=False, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey(UserModel.id))
    private = db.Column(db.Boolean(), default=True,
                        server_default="true", nullable=False)
    archive = db.Column(db.Boolean(), default=False,
                        server_default="false", nullable=False)
    tags = db.relationship(TagModel, secondary=tags, lazy='subquery', backref=db.backref('notes', lazy=True))

    @classmethod
    def get_all_notes(cls, author, archive):
        if archive == "all":
            return NoteModel.query.filter_by(author_id=author.id).all()
        if archive == "no_archive":
            return NoteModel.query.filter_by(author_id=author.id, archive=False).all()
        if archive == "archive":
            return NoteModel.query.filter_by(author_id=author.id, archive=True).all()

    @classmethod
    def get_all_public_notes(cls):
        return NoteModel.query.filter_by(private=False, archive=False).all()

    @classmethod
    def get_notes_filtered_by_tags(cls, tag_name):
        return NoteModel.query.filter(NoteModel.tags.any(name=tag_name), NoteModel.archive == False).all()

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
