import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_session import Session

# Compresión opcional
try:
    from flask_compress import Compress
    compress_available = True
except ImportError:
    compress_available = False

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('src.config')

    # 🔹 Session config
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = os.path.join(os.getcwd(), "flask_session")
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_COOKIE_NAME'] = 'moodtune_session'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = "Lax"
    app.config['SESSION_COOKIE_SECURE'] = False
    app.config['SECRET_KEY'] = 'supersecretkey'

    Session(app)

    # 🔄 Enable CORS
    CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

    # 🗃️ Initialize DB
    db.init_app(app)

    # 🌀 Enable compression (gzip by default, brotli if available)
    if compress_available:
        Compress(app)
    else:
        print("⚠️ flask-compress not available — skipping response compression.")

    # 🔗 Register Blueprints
    from src.routes import user_routes
    from src.functions.auth import auth_bp
    from src.routes.filtered_routes import filtered_bp
    from src.routes.song_routes import bp as song_routes_bp 

    app.register_blueprint(user_routes.bp, url_prefix="/users")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(filtered_bp, url_prefix="/filter")
    app.register_blueprint(song_routes_bp, url_prefix="/songs")

    return app
