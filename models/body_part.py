from db import db

class BodyPartModel(db.Model):
    __tablename__ = 'body_part'

    id = db.Column(db.String(10), primary_key=True)
    body_part = db.Column(db.String(20), unique=True, nullable=False)

    def json(self):
        return {'id': self.id, 'body_part': self.body_part}

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    