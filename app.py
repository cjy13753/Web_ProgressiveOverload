import os
from flask import Flask
from flask_restful import Api

from resources.body_part import BodyPartList

from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') # set the environment variable in .zshrc
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

db.init_app(app)
@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(BodyPartList, '/bodyparts')


if __name__ == '__main__':
    app.run(port=5000, debug=True)