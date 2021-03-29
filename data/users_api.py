from datetime import datetime
import flask
from flask import jsonify, make_response, request
from . import db_session
from .users import User

blueprint = flask.Blueprint(
    "users.api",
    __name__,
    template_folder="templates"
)


@blueprint.route("/api/users")
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            "users":
                [item.to_dict(only=("id", "surname", "name",
                                    "age", "position", "speciality",
                                    "address", "email", "modified_date")) for item in users]
        }
    )


@blueprint.route("/api/users/<int:user_id>")
def get_one_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return make_response(jsonify({"error": "Not found"}), 404)
    return jsonify(
        {
            "user": user.to_dict(only=("id", "surname", "name",
                                       "age", "position", "speciality",
                                       "address", "email", "modified_date"))
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in ["surname", "name", "age", "email", "password"]):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    if db_sess.query(User).filter(User.id == request.json.get("id")).first():
        return make_response(jsonify({"error": "id already exists"}), 400)
    user = User(
        surname=request.json["surname"],
        name=request.json["name"],
        age=request.json["age"],
        position=request.json.get("position", ""),
        speciality=request.json.get("speciality", ""),
        address=request.json.get("address", ""),
        email=request.json["email"]
    )
    user.set_password(request.json["password"])
    if request.json.get("id") is not None:
        user.id = request.json["id"]
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return make_response(jsonify({"error": "Not found"}), 404)
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route("/api/users/<int:user_id>", methods=["PUT"])
def edit_user(user_id):
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return make_response(jsonify({"error": "Not found"}), 404)
    user.surname = request.json.get("surname", user.surname)
    user.name = request.json.get("name", user.name)
    user.age = request.json.get("age", user.age)
    user.position = request.json.get("position", user.position)
    user.speciality = request.json.get("speciality", user.speciality)
    user.address = request.json.get("address", user.address)
    user.email = request.json.get("email", user.email)
    user.modified_date = datetime.now()
    if request.json.get("password") is not None:
        user.set_password(request.json["password"])
    db_sess.commit()
    return jsonify({'success': 'OK'})
