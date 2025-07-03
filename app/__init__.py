from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_migrate import Migrate
import os
from flask_cors import CORS


db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    load_dotenv()

    app = Flask(__name__)
    CORS(app)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["JWT_HEADER_NAME"] = "Authorization"
    app.config["JWT_HEADER_TYPE"] = "Bearer"

    db.init_app(app)
    jwt.init_app(app)
    migrate = Migrate(app, db)

    from .routes.main_routes import main as main_bp
    from .routes.auth_routes import auth as auth_bp
    from .routes.transaction_routes import transactions as transactions_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/")
    app.register_blueprint(transactions_bp, url_prefix="/")

    return app
