from flask_restful import Resource, reqparse

from models.exercise import ExerciseModel

parser = reqparse.RequestParser()
parser.add_argument(
    'body_part_id',
    type=str,
    required=True,
    help="This field cannot be left blank"
)
parser.add_argument(
    'user_id',
    type=int,
    required=True,
    help="This field cannot be left blank"
)

class ExerciseList(Resource):
    def get(self):
        return {"exercises": [exercise.json() for exercise in ExerciseModel.find_all()]}

class ExerciseListForUser(Resource):
    def get(self):
        data = parser.parse_args()
        body_part_id = data['body_part_id']
        user_id = data['user_id']
        return {"exercises": [exercise.json() for exercise in ExerciseModel.find_by_body_and_user(body_part_id=body_part_id, user_id=user_id)]}

class Exercise(Resource):
    def get(self, exercise_name):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'user_id',
            type=int,
            required=True,
            help="This field cannot be left blank"
        )
        data = parser.parse_args()
        user_id = data['user_id']
        exercise = ExerciseModel.find_by_exercise_name_and_user(exercise_name=exercise_name, user_id=user_id)
        if exercise:
            return exercise.json()
        return {'message': 'exercise name not found'}, 404

    def post(self, exercise_name):
        data = parser.parse_args()
        body_part_id = data['body_part_id']
        user_id = data['user_id']

        if ExerciseModel.find_by_exercise_name_and_user(exercise_name=exercise_name, user_id=user_id):
            return {"message": "The exercise name, {}, already exists.".format(exercise_name)}, 400
        
        exercise = ExerciseModel(exercise_name=exercise_name, body_part_id=body_part_id, user_id=user_id)
        try:
            exercise.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return exercise.json(), 201