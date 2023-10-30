#!/usr/bin/python3
"""
Flask App that integrates with AirBnB static HTML Template
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage, Place, Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_amenities(place_id):
    """Retrieve the list of all Amenity objects of a Place"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    if storage.__class__.__name__ == 'DBStorage':
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [storage.get('Amenity', amenity_id).to_dict() for amenity_id in place.amenity_ids]
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(place_id, amenity_id):
    """Deletes an Amenity object from a Place"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    if storage.__class__.__name__ == 'DBStorage':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
        storage.save()
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)
        storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def link_amenity(place_id, amenity_id):
    """Links an Amenity object to a Place"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    if storage.__class__.__name__ == 'DBStorage':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
        storage.save()
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)
        storage.save()
    return jsonify(amenity.to_dict()), 201
