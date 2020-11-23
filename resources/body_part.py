from flask_restful import Resource

from models.body_part import BodyPartModel

class BodyPartList(Resource):
    def get(self):
        return {"bodies": [body.json() for body in BodyPartModel.find_all()]}