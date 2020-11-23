from db import db

class WorkoutRecordModel(db.Model):
    __tablename__ = 'workout_record'

    id = db.Column(db.Integer, primary_key=True)
    set_number = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)

    def json(self):
        return {
            'id': self.id,
            'set_number': self.set_number,
            'weight': self.weight,
            'reps': self.reps,
            'created_on': self.created_on.strftime("%Y/%m/%d"),
            'exercise_id': self.exercise_id
        }
    
    @classmethod
    def addarg(cls, argument):
        return {"name": argument, "type": int, "required": True, "help": "This field cannot be left blank"}

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()   