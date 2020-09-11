#!/usr/bin/python3
"""view for Place objects that handles all default RestFul API"""
import os
import json
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=["GET"])
def get_places(city_id=None):
    """retrieves the list of all Place objects of a City"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route("/places/<place_id>", methods=["GET"])
def get_place_id(place_id):
    """retrieves a Place object"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"])
def del_place_id(place_id):
    """deletes a Place object"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def post_places(city_id):
    """creates a Place"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    my_request = request.get_json()
    if not my_request:
        abort(400, "Not a JSON")
    if "user_id" not in my_request:
        abort(400, "Missing user_id")
    user_id = my_request["user_id"]
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    if "name" not in my_request:
        abort(400, "Missing name")
    place = Place(**my_request)
    setattr(place, "city_id", city_id)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"])
def put_place_id(place_id):
    """updates a Place object"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    my_request = request.get_json()
    if not my_request:
        abort(400, "Not a JSON")
    ignore_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for key, value in my_request.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def places_search():
    """
    Retrieves all Place objects depending of the JSON in the body
    of the request
    """

    if request.get_json() is None:
        abort(400, "Not a JSON")

    search_p = request.get_json()

    if search_p and len(search):
        states = search_p.get('states', None)
        cities = search_p('cities', None)
        amenities = search_p('amenities', None)

    if not search_p or not len(search_p) or (
            not states and
            not cities and
            not amenities):
        places = storage.all(Place).values()
        list_places = []
        for place in places:
            list_places.append(place.to_dict())
        return jsonify(list_places)

    list_places = []
    if states:
        states_obj = [storage.get(State, s_id) for s_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)

    if cities:
        city_obj = [storage.get(City, c_id) for c_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    if amenities:
        if not list_places:
            list_places = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, p_id) for p_id in amenities]
        list_places = [place for place in list_places
                       if all([am in place.amenities
                               for am in amenities_obj])]

    places = []
    for p in list_places:
        d = p.to_dict()
        d.pop('amenities', None)
        places.append(d)

    return jsonify(places)
