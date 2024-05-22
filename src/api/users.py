from flask_restx import Api, Resource, fields

from flask import Blueprint, request
from src import db
from src.api.models import User

users_blueprint = Blueprint("users", __name__)
api = Api(users_blueprint)
user = api.model(
    "User",
    {
        "id": fields.Integer(readOnly=True),
        "username": fields.String(required=True),
        "email": fields.String(required=True),
        "created_date": fields.DateTime,
    },
)


class UsersList(Resource):
    @api.marshal_with(user, as_list=True)
    def get(self):
        return User.query.all(), 200

    @api.expect(user, validate=True)
    def post(self):
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")

        response_object = {}
        if User.query.filter_by(email=email).first():
            response_object["message"] = "Sorry. That email already exists."
            return response_object, 400

        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()

        response_object = new_user.to_dict()

        return response_object, 201


class UsersDetail(Resource):

    @api.marshal_with(user)
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            api.abort(404, f"User {user_id} does not exist")
        return user, 200


api.add_resource(UsersList, "/users")
api.add_resource(UsersDetail, "/users/<int:user_id>")
