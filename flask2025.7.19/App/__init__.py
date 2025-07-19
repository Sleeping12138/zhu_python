from flask import Flask
from App.route.test import bp


# Define a function called create_app
def create_app():
    # Create an instance of the Flask class
    app = Flask(__name__)

    app.register_blueprint(blueprint=bp)

    # Return the app instance
    return app
