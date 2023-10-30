#!/usr/bin/python3
"""
Flask App that integrates with AirBnB static HTML Template
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage, State


@app_views.route('/states', methods=['GET'])
def get_states():
    """Retrieve the list of all State objects"""
    states = storage.all('State').values()
    states_list = [state.to_dict() for state in states]
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """Retrieve a State object"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State object"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'])
def create_state():
    """Creates a State"""
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    state = State(**request.json)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Updates a State object"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    for key, value in request.json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict())


