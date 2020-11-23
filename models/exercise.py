from db import db

class ExerciseModel(db.Model):
    __tablename__ = 'exercise'

    id = db.Column(db.Integer, primary_key=True)
    exercise_name = db.Column(db.String(50), unique=True, nullable=False)
    body_part_id = db.Column(db.String(10), db.ForeignKey('body_part.id'))
    body_part = db.relationship('BodyPartModel')

    def json(self):
        return {'id': self.id, 'exercise_name': self.exercise_name, 'body_part_id': self.body_part_id}
    
    @classmethod
    def find_by_exercise_name(cls, exercise_name):
        return cls.query.filter_by(exercise_name=exercise_name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    