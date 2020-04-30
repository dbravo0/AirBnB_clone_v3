#!/usr/bin/python3
"""view for User object that handles all default RestFul API"""
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """retrieves the list of all User objects"""
    users = storage.all(User)
    return jsonify([user.to_dict() for user in users.values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_id(user_id):
    """retrieves a User object"""
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_user_id(user_id):
    """deletes a User object"""
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_users():
    """creates a User object"""
    new_user = request.get_json()
    if not new_user:
        abort(400, "Not a JSON")
    if "email" not in new_user:
        abort(400, "Missing email")
    if "password" not in new_user:
        abort(400, "Missing password")
    user = User(**new_user)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user_id(user_id):
    """updates a User object"""
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    my_dict = request.get_json()
    if not my_dict:
        abort(400, "Not a JSON")
    for key, value in my_dict.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
