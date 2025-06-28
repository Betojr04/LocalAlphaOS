from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User

main = Blueprint("main", __name__)


@main.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify({"message": f"Welcome, {user.id}!"}), 200
