from flask_restful import Resource, reqparse

from models.exercise import ExerciseModel

class ExerciseList(Resource):
    def get(self):
        return {"exercises": [exercise.json() for exercise in ExerciseModel.find_all()]}

class Exercise(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'body_part_id',
        type=str,
        required=True,
        help="This field cannot be left blank"
    )
    
    def get(self, exercise_name):
        exercise = ExerciseModel.find_by_exercise_name(exercise_name)
        if exercise:
            return exercise.json()
        return {'message': 'exercise name not found'}, 404

    def post(self, exercise_name):
        if ExerciseModel.find_by_exercise_name(exercise_name):
            return {"message": "The exercise name, {}, already exists.".format(exercise_name)}, 400

        data = Exercise.parser.parse_args()
        exercise = ExerciseModel(exercise_name=exercise_name, body_part_id=data['body_part_id'])
        print(exercise_name)
        try:
            exercise.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return exercise.json(), 201