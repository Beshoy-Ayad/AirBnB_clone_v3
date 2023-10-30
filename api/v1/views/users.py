#!/usr/bin/python3
"""
Flask App that integrates with AirBnB static HTML Template
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage, User


@app_views.route('/users', methods=['GET'])
def get_users():
    """Retrieve the list of all User objects"""
    users = storage.all('User').values()
    users_list = [user.to_dict() for user in users]
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieve a User object"""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'])
def create_user():
    """Creates a User"""
    if not request.json:
        abort(400, 'Not a JSON')
    if 'email' not in request.json:
        abort(400, 'Missing email')
    if 'password' not in request.json:
        abort(400, 'Missing password')
    user = User(**request.json)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates a User object"""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    for key, value in request.json.items():
        if key not in ['id', 'email', 'password', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict())
