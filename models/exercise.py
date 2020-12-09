from db import db

class ExerciseModel(db.Model):
    __tablename__ = 'exercise'

    id = db.Column(db.Integer, primary_key=True)
    exercise_name = db.Column(db.String(50), unique=True, nullable=False)
    body_part_id = db.Column(db.String(10), db.ForeignKey('body_part.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    body_part = db.relationship('BodyPartModel')


    def json(self):
        return {'id': self.id, 'exercise_name': self.exercise_name, 'body_part_id': self.body_part_id, 'user_id': self.user_id, 'body_part': self.body_part.body_part_name} # self.body_part is an BodyPartModel instance.
    
    @classmethod
    def find_by_exercise_name_and_user(cls, exercise_name, user_id):
        return cls.query.filter_by(exercise_name=exercise_name, user_id=user_id).first()

    @classmethod
    def find_by_body_and_user(cls, body_part_id, user_id):
        return cls.query.filter_by(body_part_id=body_part_id, user_id=user_id)

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    