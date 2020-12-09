from flask_restful import Resource, reqparse

from models.workout_record import WorkoutRecordModel

class WorkoutRecordList(Resource):
    def get(self):
        return {"workout_records": [workout_record.json() for workout_record in WorkoutRecordModel.find_all()]}


class WorkoutRecord(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument(**WorkoutRecordModel.addarg('set_number', int))
    parser.add_argument(**WorkoutRecordModel.addarg('weight', float))
    parser.add_argument(**WorkoutRecordModel.addarg('reps', int))
    parser.add_argument(**WorkoutRecordModel.addarg('exercise_id', int))
        
    def post(self):
        data = WorkoutRecord.parser.parse_args()
        workout_record = WorkoutRecordModel(**data)
        try:
            workout_record.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return workout_record.json(), 201


class WorkoutRecordTable(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument(**WorkoutRecordModel.addarg('exercise_id', int))
        
    def get(self):
        data = WorkoutRecordTable.parser.parse_args()
        print(data)
        return WorkoutRecordModel.get_table(**data)