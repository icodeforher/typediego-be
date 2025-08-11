from flask import Flask
from flask_cors import CORS
from app.core.config import Config
from app.routes.chatbot import chatbot_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configure CORS for specific origins
    CORS(app, resources={
        r"/api/*": {
            "origins": ["https://typediego.com", "http://localhost:3000"],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "X-API-KEY"]
        }
    })
    
    # Register blueprints
    app.register_blueprint(chatbot_bp, url_prefix='/api')
    
    return app
