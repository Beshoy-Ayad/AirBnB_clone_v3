#!/usr/bin/python3

"""
Flask App that integrates with AirBnB static HTML Template
"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    """Return the status of the API"""
    return jsonify({'status': 'OK'})
