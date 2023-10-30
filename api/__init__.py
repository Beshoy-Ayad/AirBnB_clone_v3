#!/usr/bin/python3
"""
Flask App that integrates with AirBnB static HTML Template
"""

from flask import Flask
from api.v1.app import app as app_v1


app = Flask(__name__)
app.register_blueprint(app_v1, url_prefix='/api/v1')


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
