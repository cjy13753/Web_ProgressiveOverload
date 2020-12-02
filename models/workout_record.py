from flask import jsonify
from db import db
import pandas as pd

class WorkoutRecordModel(db.Model):
    __tablename__ = 'workout_record'
    __table_args__ = (
        db.UniqueConstraint('set_number', 'created_on', 'exercise_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    set_number = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    created_on = db.Column(db.Date, server_default=db.func.now())
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
    def addarg(cls, argument, datatype):
        return {"name": argument, "type": datatype, "required": True, "help": "This field cannot be left blank"}

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod    
    def get_table(cls, exercise_id):
        query = ''' 
            SELECT set_number, weight, reps, created_on FROM workout_record 
            WHERE exercise_id={} AND created_on in (SELECT DISTINCT created_on FROM workout_record WHERE exercise_id={} ORDER BY created_on DESC LIMIT 3);
        '''.format(exercise_id, exercise_id)
        result = db.session.execute(query)
        rows = []
        for r in result:
            rows.append(dict(r.items()))

        df = pd.DataFrame(rows)
        df.rename(columns={'weight':'0_wgt'}, inplace=True)
        df.rename(columns={'reps':'1_rep'}, inplace=True)
        df.created_on = pd.to_datetime(df.created_on)
        df.created_on = df.created_on.dt.strftime('%m-%d')
        created_on = df['created_on'].unique()
        df_reshaping_melted = df.melt(id_vars=['created_on', 'set_number'])
        df_reshaping_pivoting = df_reshaping_melted.pivot(index=['set_number', 'variable'], columns='created_on', values='value').reset_index()
        df_pivoting_after_reshaping = df_reshaping_pivoting.pivot(index='set_number', columns='variable', values=created_on).fillna('-')
                
        return jsonify({"response": df_pivoting_after_reshaping.to_html()})