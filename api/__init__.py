from flask import Flask
from api.v1.app import app_views
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Close the database connection after each request"""
    storage.close()
