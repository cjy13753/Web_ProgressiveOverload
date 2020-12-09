import os
from flask import Flask
from flask_restful import Api
from flask_login import LoginManager

# from security import authenticate, identity
from resources.body_part import BodyPartList, BodyPart
from resources.exercise import ExerciseList, Exercise, ExerciseListForUser
from resources.workout_record import WorkoutRecordList, WorkoutRecord, WorkoutRecordTable

from models.user import UserModel

from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') # set the environment variable in .zshrc
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = os.environ.get('SECRET_KEY') # key to both encrypt and decrypt the messages (used for jwt)
api = Api(app)

db.init_app(app)
@app.before_first_request
def create_tables():
    db.create_all() 

from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from main import main as main_blueprint
app.register_blueprint(main_blueprint)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return UserModel.find_by_id(int(user_id))


api.add_resource(BodyPartList, '/bodyparts')
api.add_resource(BodyPart, '/body_part/<string:body_part_name>')
api.add_resource(ExerciseList, '/exercises')
api.add_resource(ExerciseListForUser, '/exercisesforuser')
api.add_resource(Exercise, '/exercise/<string:exercise_name>')
api.add_resource(WorkoutRecordList, '/workoutrecords')
api.add_resource(WorkoutRecord, '/workout_record')
api.add_resource(WorkoutRecordTable, '/workout_record_table')

if __name__ == '__main__':
    app.run(port=5000, debug=True)