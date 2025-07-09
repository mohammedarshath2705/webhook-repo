from flask import Flask
from .extensions import mongo
from .webhook.routes import webhook_bp

def create_app():
    app = Flask(__name__)

    # MongoDB config
    app.config["MONGO_URI"] = "mongodb://localhost:27017/github_events"

    # Initialize Mongo
    mongo.init_app(app)

    # Register Blueprints
    app.register_blueprint(webhook_bp)

    return app
