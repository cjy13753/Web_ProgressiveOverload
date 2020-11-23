from db import db

class BodyPartModel(db.Model):
    __tablename__ = 'body_part'

    id = db.Column(db.String(10), primary_key=True)
    body_part_name = db.Column(db.String(20), unique=True, nullable=False)

    def json(self):
        return {'id': self.id, 'body_part_name': self.body_part_name}
    
    @classmethod
    def find_by_body_part_name(cls, body_part_name):
        return cls.query.filter_by(body_part_name=body_part_name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    