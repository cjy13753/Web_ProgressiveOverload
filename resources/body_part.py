from flask_restful import Resource, reqparse

from models.body_part import BodyPartModel

class BodyPartList(Resource):
    def get(self):
        return {"body_parts": [body.json() for body in BodyPartModel.find_all()]}

class BodyPart(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'id',
        type=str,
        required=True,
        help="This field cannot be left blank"
    )
    
    def get(self, body_part_name):
        body_part = BodyPartModel.find_by_body_part_name(body_part_name)
        if body_part:
            return body_part.json()
        return {'message': 'body-part name not found'}, 404

    def post(self, body_part_name):
        if BodyPartModel.find_by_body_part_name(body_part_name):
            return {"message": "The body-part name, {}, already exists.".format(body_part_name)}, 400

        data = BodyPart.parser.parse_args()
        body_part = BodyPartModel(id=data["id"], body_part_name=body_part_name)
        try:
            body_part.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return body_part.json(), 201