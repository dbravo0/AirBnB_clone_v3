#!/usr/bin/python3
"""api"""
import os
from flask import Flask, Blueprint, jsonify
from api.v1.views import app_views
from models import storage
from flask_cors import CORS


app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_app(code):
    """method Handles teardown"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """handler for 404 errors that returns a JSON"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
